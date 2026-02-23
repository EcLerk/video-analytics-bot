from sqlalchemy import text
from app.db.session import Session
from app.exceptions.exceptions import UnsafeSQLError, NotFoundError, DatabaseQueryError


def _validate_sql(sql: str) -> None:
    sql_upper = sql.strip().upper()
    if not sql_upper.startswith("SELECT"):
        raise UnsafeSQLError(f"Only SELECT queries are allowed")
    forbidden = {"INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER"}
    if any(keyword in sql_upper for keyword in forbidden):
        raise UnsafeSQLError("Query contains forbidden keywords")


async def execute_query(sql: str) -> str:
    _validate_sql(sql)
    async with Session() as session:
        try:
            result = await session.execute(text(sql))
            row = result.fetchone()
            if row is None:
                raise NotFoundError()
            return str(row[0])
        except UnsafeSQLError:
            raise
        except Exception as e:
            raise DatabaseQueryError(f"Query execution failed") from e
        