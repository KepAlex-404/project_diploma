from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)

empty_body_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="WRONG JSON body",
)

no_model = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="No such model",
)
