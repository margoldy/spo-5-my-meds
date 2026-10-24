from app.db.models import Base
from app.db.seed_medications import seed_medications
from app.db.session import engine


def create_tables():
    Base.metadata.create_all(bind=engine)
    seed_medications()


if __name__ == "__main__":
    create_tables()
