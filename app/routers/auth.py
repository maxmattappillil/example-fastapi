from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from .. import schemas, models, utils
from ..database import get_db

from .. import oauth2

from fastapi.responses import JSONResponse

router = APIRouter(tags=["Authentication"])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # Find the user
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # Compare the two hashes of the raw password and the hashed password we have in the DB
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # Create Token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # Sending back a response with the token as an HTTP-Only cookie
    # response = JSONResponse(content={"message": "Login successful"})
    # response.set_cookie(key="access_token", value=access_token,
    #                     httponly=True, samesite="Strict")

    # return response

    # Return Token
    return {"access_token": access_token, "token_type": "bearer"}