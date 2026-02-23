class NotFoundError(Exception):
    """Raised when query returns no results"""
    default_message = "No data found for the given query"

    def __init__(self, message: str = default_message):
        super().__init__(message)


class LLMError(Exception):
    """Raised when LLM fails to generate SQL"""
    default_message = "Failed to generate SQL from user input"

    def __init__(self, message: str = default_message):
        super().__init__(message)


class DatabaseQueryError(Exception):
    """Raised when generated SQL query fails"""
    default_message = "Database query execution failed"

    def __init__(self, message: str = default_message):
        super().__init__(message)


class UnsafeSQLError(DatabaseQueryError):
    """Raised when generated SQL contains forbidden keywords"""
    default_message = "Generated SQL contains forbidden keywords"

    def __init__(self, message: str = default_message):
        super().__init__(message)

