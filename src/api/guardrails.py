def validate_sql(sql: str) -> bool:
    forbidden = ["DROP", "DELETE", "UPDATE"]
    for keyword in forbidden:
        if keyword in sql.upper():
            return False
    return True
