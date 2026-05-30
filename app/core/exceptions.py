class AppException(Exception):
    """Base exception for application-specific errors."""
    # In Python, this class inherits from built-in Exception.
    # That means every subclass of AppException is also an Exception.
    pass


class EntityNotFound(AppException):
    """Raised when a requested resource is not found (404)."""

    def __init__(self, entity_name: str, entity_id: int | str = None):
        # In EntityNotFound, __init__ runs when you do EntityNotFound("Member", 5).
        # self refers to the current instance of the class.
        if entity_id:
            self.detail = f"{entity_name} with id '{entity_id}' not found"
            # In EntityNotFound, self.detail = ... attaches detail to the exception object.
            # self.detail is a custom attribute we add to carry an error message.
        else:
            self.detail = f"{entity_name} not found"

        # `super()` gives access to the parent class (AppException -> Exception).
        # Calling `super().__init__(self.detail)` initializes the built-in Exception
        # base class with the same message so the exception behaves like a normal
        # Python exception.
        super().__init__(self.detail)
        # super().__init__(self.detail) calls the base class initializer.
        # Calling super().__init__(self.detail) ensures the base Exception stores the message.


class DuplicateResource(AppException):
    """Raised when a unique constraint is violated (409)."""

    def __init__(self, field: str, value: str):
        self.detail = f"{field} '{value}' already exists"
        super().__init__(self.detail)


class BadRequestError(AppException):
    """Raised for invalid business logic or validation (400)."""

    def __init__(self, message: str):
        self.detail = message
        super().__init__(self.detail)


class InternalServerError(AppException):
    """Raised for unexpected server-side errors (500)."""

    def __init__(self,  message: str = "Internal server error"):
        self.detail = message
        super().__init__(self.detail)
