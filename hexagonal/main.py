from config.wiring import build_app


def wsgi():
    return build_app()
