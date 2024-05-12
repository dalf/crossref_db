from sqlmodel import SQLModel, Session, create_engine


ENGINE = None


def get_session() -> Session:
    return Session(ENGINE)


def get_engine():
    return ENGINE


def connect_db(db_url):
    global ENGINE
    ENGINE = create_engine(db_url)


def create_db():
    SQLModel.metadata.create_all(ENGINE)
