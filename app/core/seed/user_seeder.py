# seeder.py
from app.core.database import Base, SessionLocal, engine
from app.models.user.user import User
from app.models.user.user_role import UserRole

# Create tables (if not already created)
Base.metadata.create_all(bind=engine)

# Open a session
db = SessionLocal()

# Seed roles
roles = ["superadmin", "admin", "staff"]
for role_name in roles:
    if not db.query(UserRole).filter(UserRole.name == role_name).first():
        new_role = UserRole(name=role_name)
        db.add(new_role)
db.commit()

# Seed an admin user
if not db.query(User).filter(User.username == "admin").first():
    admin_role = db.query(UserRole).filter(UserRole.name == "admin").first()
    admin_user = User(
        username="admin",
        email="admin@example.com",
        full_name="Administrator",
        hashed_password=User.get_password_hash("admin123"),
        role_id=admin_role.id
    )
    db.add(admin_user)
    db.commit()

db.close()
print("Seeding complete!")
