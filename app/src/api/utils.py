from functools import wraps
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.types.standard_response import StandardResponse
from src.db import engine


def get_db_session():
    with Session(engine) as session:
        yield session


def exception_wrapper(
    error_message: str | None = None,
    catch_http_exc: bool = False,
):
    def decorator(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException as e:
                if catch_http_exc:
                    return StandardResponse(
                        success=False,
                        message=e.detail,
                        data={"error_code": e.status_code},
                    )
                else:
                    raise
            except Exception as e:
                if error_message is None:
                    message = str(e)
                else:
                    message = f"{error_message}: {str(e)}"
                return StandardResponse(
                    success=False,
                    message=message,
                    data={"error_code": 500},
                )

        return wrapped

    return decorator
