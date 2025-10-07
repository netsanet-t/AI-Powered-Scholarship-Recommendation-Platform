from fastapi import status

class NEXTstepApiExeption(Exception):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code

class IncorrectCredentials(NEXTstepApiExeption):
    def __init__(self, detail: str | None):
        super().__init__(detail=detail or "Incorrect Credentials", status_code=status.HTTP_401_UNAUTHORIZED)

class NotFoundExeption(NEXTstepApiExeption):
    def __init__(self, name: str):
        super().__init__(detail=f"{name} not found!", status_code=status.HTTP_404_NOT_FOUND)

class NotAuthenticated(NEXTstepApiExeption):
    def __init__(self):
        super().__init__(detail="Not Authenticated", status_code=status.HTTP_403_FORBIDDEN)

class NotAuthorizedException(NEXTstepApiExeption):
    def __init__(self):
        super().__init__(detail="Not Authorized", status_code=status.HTTP_401_UNAUTHORIZED)