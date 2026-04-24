from pydantic import BaseModel, Field
from typing import Any


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, description="Natural-language business question")
    execute: bool = Field(default=False, description="When true, execute validated SQL against configured warehouse")


class QueryResponse(BaseModel):
    question: str
    retrieved_context: list[dict[str, Any]]
    generated_sql: str
    is_sql_valid: bool
    execution_mode: str
    result: list[dict[str, Any]]
    warnings: list[str]
