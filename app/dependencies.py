from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
import jwt

from core.database import SessionLocal

from core.services.token import ALGORITHM, SECRET_KEY, TokenData
from core.models import Trainer


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Token auth dependency

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_trainer(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    trainer = Trainer.get_trainer_by_username(db, username=token_data.username)
    if trainer is None:
        raise credentials_exception
    return trainer