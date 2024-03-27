from yatg.settings import Settings


def initialize_db():
    """
    Create db
    Create tables
    """
    settings = Settings()
    fp = settings.db_path
    return fp

