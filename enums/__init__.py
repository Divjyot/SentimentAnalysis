import enum


class API_ENV(enum.Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class API_CONFIG(enum.Enum):
    SECRET_KEY = "SECRET_KEY"
    DEBUG = "DEBUG"
    TESTING = "TESTING"
