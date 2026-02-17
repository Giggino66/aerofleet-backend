import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import Base, engine, SessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.aircraft import Aircraft  # ensure table is registered


def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            db.add(User(
                username="admin",
                email="admin@aerofleet.local",
                password_hash=hash_password("admin123"),
                full_name="Administrator",
                role="admin",
                is_active=True,
            ))
            db.commit()
            print("✓ Admin user created  (username: admin / password: admin123)")
            print("⚠️  CHANGE PASSWORD AFTER FIRST LOGIN!")
        else:
            print("✓ Admin user already exists")
    finally:
        db.close()

    print("✓ Database ready")


if __name__ == "__main__":
    init_db()
