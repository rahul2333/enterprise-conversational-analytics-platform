from fastapi import FastAPI

from src.ai_engine.gemini_provider import GeminiProvider
from src.api.guardrails import validate_sql
from src.core.config import settings
from src.core.models import QueryRequest, QueryResponse
from src.data.bigquery_executor import BigQueryExecutor
from src.retrieval.vector_search import VectorSearch
from src.security.sql_guardrails import validate_read_only_sql

app = FastAPI(title="Enterprise Conversational Analytics API")

# Initialize providers
llm = GeminiProvider()
retriever = VectorSearch()
executor = None

if getattr(settings, "bq_project", None):
    try:
        executor = BigQueryExecutor(project=settings.bq_project)
    except Exception:
        executor = None


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    warnings: list[str] = []

    # 1) Retrieve metadata/context
    context = retriever.search(req.question)
    context_list = context if isinstance(context, list) else [context]

    # 2) Generate SQL via LLM provider
    sql = llm.generate_sql(req.question, str(context_list))

    # 3) Validate SQL (guardrails)
    is_valid = validate_sql(sql)
    if is_valid:
        try:
            validate_read_only_sql(sql)
        except ValueError as exc:
            is_valid = False
            warnings.append(str(exc))

    if not is_valid and not warnings:
        warnings.append("SQL failed validation; execution blocked")

    # 4) Execute (optional)
    result: list[dict] = []
    execution_mode = "dry_run"

    if req.execute:
        if not is_valid:
            execution_mode = "blocked"
        elif executor is None:
            execution_mode = "unavailable"
            warnings.append("No warehouse executor configured")
        else:
            try:
                result = executor.execute(sql)
                execution_mode = "executed"
            except Exception as e:
                execution_mode = "error"
                warnings.append(str(e))

    return QueryResponse(
        question=req.question,
        retrieved_context=context_list,
        generated_sql=sql,
        is_sql_valid=is_valid,
        execution_mode=execution_mode,
        result=result,
        warnings=warnings,
    )
