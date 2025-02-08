from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, User, UserUpdate
from app.actions.user import get_user, get_users, create_user, update_user, delete_user, get_user_by_email
from app.services.ghilbi import get_ghibli_data
from app.db.session import get_db
from sqlalchemy.exc import IntegrityError 

router = APIRouter()

# Endpoints para usuarios
@router.post("/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    # Validar que el email no esté duplicado
    db_user_by_email = get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Intentar crear el usuario
    try:
        return create_user(db, user=user)
    except IntegrityError as e:
        # Capturar errores de integridad de la base de datos (por ejemplo, ID duplicado)
        raise HTTPException(
            status_code=400,
            detail="Duplicate ID or other database integrity error"
        )
    except Exception as e:
        # Capturar otros errores inesperados
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=User)
def update_user_endpoint(
    user_id: int,
    user: UserUpdate, 
    db: Session = Depends(get_db)
):
    db_user = update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=User)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

VALID_RESOURCES_BY_ROLE = {
    "admin": ["films", "people", "locations", "species", "vehicles"],
    "films": ["films"],
    "people": ["people"],
    "locations": ["locations"],
    "species": ["species"],
    "vehicles": ["vehicles"],
}

# Endpoint para consumir Studio Ghibli API según el rol del usuario
@router.get("/{user_id}/ghibli/{resource}")
def consume_ghibli_api(
    user_id: int,
    resource: str,
    db: Session = Depends(get_db)
):
    # Obtener el usuario
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Validar que el recurso solicitado coincida con el rol del usuario
    valid_resources = VALID_RESOURCES_BY_ROLE.get(db_user.role, [])
    
    if resource not in valid_resources:
        raise HTTPException(
            status_code=403,
            detail=f"User with role '{db_user.role}' is not allowed to access '{resource}'"
        )

    # Consumir la API de Studio Ghibli
    try:
        ghibli_data = get_ghibli_data(resource)
        return ghibli_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))