class QueryEmptyNoneValueError(Exception):
    """Exception raised
    if `query` parameter is Empty or None
    """

    def __init__(self, query: str, message="Query cannot be empty or None", *args: object) -> None:
        self.query = query
        self.message = message
        super().__init__(*args)

    def __str__(self):
        return f"{self.query} -> {self.message}"


class QueryTypeError(Exception):
    """Exception raised
    if `query` is of type other than str
    """

    def __init__(self, query: str, message="Query can only be of str type", *args: object) -> None:
        self.query = query
        self.message = message
        super().__init__(*args)

    def __str__(self):
        return f"{self.query} -> {self.message}"


class AuthenticationError(Exception):
    """Exception raised
    if SECRET_KEY do not match or present in request header
    """

    def __init__(self, query: str, message="Unauthorised access.", *args: object) -> None:
        self.query = query
        self.message = message
        super().__init__(*args)

    def __str__(self):
        return f"{self.query} -> {self.message}"
    