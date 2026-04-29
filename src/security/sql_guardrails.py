def _strip_leading_comments(sql: str) -> str:
    """Remove leading SQL comments so read-only checks inspect the first statement."""
    remaining = sql.strip()

    while remaining.startswith("--"):
        newline_idx = remaining.find("\n")
        if newline_idx == -1:
            return ""
        remaining = remaining[newline_idx + 1 :].lstrip()

    return remaining


def validate_read_only_sql(sql: str) -> None:
    normalized = _strip_leading_comments(sql).lower()
    if not normalized.startswith("select"):
        raise ValueError("Only read-only SELECT statements are allowed.")
    if ";" in normalized[:-1]:
        raise ValueError("Multiple SQL statements are not allowed.")
