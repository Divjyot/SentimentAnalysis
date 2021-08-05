#'''WSGI entry'''
import app
from decouple import config
from enums import API_ENV

# Creates the client app based on ENVIRONMENT
handler = app.create_app(config(API_ENV.__name__, API_ENV.DEVELOPMENT.value) == API_ENV.PRODUCTION.value)


def main():
    # Entry point when run via Python interpreter.
    print("== Running in debug mode ==")
    debug_api_host = "0.0.0.0"
    debug_api_port = "80"
    app.create_app(is_prod=False).run(host=debug_api_host, port=debug_api_port, debug=True)


if __name__ == "__main__":
    main()
