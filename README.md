# Enterprise Conversational Analytics Platform

Enterprise-grade conversational analytics reference implementation on Google Cloud Platform. The platform enables natural-language questions over governed analytical datasets using a semantic metadata layer, retrieval-augmented generation, validated SQL generation, BigQuery execution, and a secure API surface.

> This is a public portfolio project.

## Objectives

- Demonstrate a production-oriented architecture for conversational analytics.
- Show how metadata, semantic definitions, and governance can improve NLQ-to-SQL reliability.
- Provide a modular implementation that can be extended to different LLMs, vector databases, and data warehouses.
- Present architecture, security, cost, and operational trade-offs in a way suitable for enterprise architect interviews.

## Reference Architecture

User → UI → API → Retrieval + AI Engine → SQL Validation → BigQuery → Response

## Key Capabilities

- Natural-language question intake
- Metadata-driven retrieval
- LLM-assisted SQL generation
- Query validation and execution
- Modular architecture

## Tech Stack

- FastAPI
- Streamlit
- BigQuery (optional integration)
- Pluggable LLM provider
- Pluggable vector DB

## Run Locally

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

## License

MIT
