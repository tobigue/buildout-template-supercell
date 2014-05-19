from .service import HelloWorldService


def start_app():
    service = HelloWorldService()
    service.main()
