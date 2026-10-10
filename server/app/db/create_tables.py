from app.db.models import Base
from app.db.session import engine


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
