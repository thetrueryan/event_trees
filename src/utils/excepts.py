from fastapi import HTTPException, status


unknown_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Server error"
)

not_found_error = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Page not found"
)

forbidden_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="access forbidden"
)