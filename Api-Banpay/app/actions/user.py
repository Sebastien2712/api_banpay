from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    # Obtener el usuario de la base de datos
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None  # Usuario no encontrado

    # Actualizar solo los campos permitidos
    if user.username is not None:
        db_user.username = user.username
    if user.role is not None:
        db_user.role = user.role

    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    # Buscar el usuario en la base de datos
    db_user = db.query(User).filter(User.id == user_id).first()
    
    # Si el usuario no existe, retornar None
    if db_user is None:
        return None
    
    # Eliminar el usuario
    db.delete(db_user)
    db.commit()
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()