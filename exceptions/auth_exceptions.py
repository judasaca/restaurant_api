from fastapi import HTTPException, status

InvalidLoginCredentialsException = HTTPException(
    status.HTTP_401_UNAUTHORIZED, "Invalid email or password"
)
