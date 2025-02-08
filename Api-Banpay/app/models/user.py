from sqlalchemy import Column, Integer, String, Enum
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum("admin", "films", "people", "locations", "species", "vehicles", name="role_enum"))
    