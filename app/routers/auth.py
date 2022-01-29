from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from .. import database, models, utils, schemas


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not utils.verify_str(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return {"access_token": "example token"}
