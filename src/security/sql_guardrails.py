def validate_read_only_sql(sql: str) -> None:
    normalized = sql.strip().lower()
    if not normalized.startswith("select"):
        raise ValueError("Only read-only SELECT statements are allowed.")
    if ";" in normalized[:-1]:
        raise ValueError("Multiple SQL statements are not allowed.")
