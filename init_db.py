"""Initialize database with default data"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models.user import User
from app.models.aircraft import Aircraft


def init_db():
    """Initialize database"""
    
    print("=" * 60)
    print("AeroFleet Manager - Database Initialization")
    print("=" * 60)
    
    try:
        print("\nCreating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created")
        
        db = SessionLocal()
        
        try:
            # Create admin user
            admin = db.query(User).filter(User.username == "admin").first()
            
            if not admin:
                print("\nCreating admin user...")
                admin = User(
                    username="admin",
                    email="admin@aerofleet.local",
                    password_hash=get_password_hash("admin123"),
                    full_name="Administrator",
                    role="admin",
                    is_active=True
                )
                db.add(admin)
                db.commit()
                print("✓ Admin user created")
                print("\n" + "=" * 60)
                print("DEFAULT CREDENTIALS:")
                print("Username: admin")
                print("Password: admin123")
                print("⚠️  CHANGE PASSWORD AFTER FIRST LOGIN!")
                print("=" * 60)
            else:
                print("✓ Admin user already exists")
            
            print("\n✓ Database initialization completed!\n")
            
        except Exception as e:
            print(f"✗ Error during initialization: {e}")
            db.rollback()
            raise
        finally:
            db.close()
            
    except Exception as e:
        print(f"✗ Failed to initialize database: {e}")
        raise


if __name__ == "__main__":
    init_db()
