from fastapi import FastAPI, Depends, HTTPException, status, Body, UploadFile, File, APIRouter
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
#from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
###  get_current_user  get_current_user_admin
#get_tts_client, get_stt_client
from schemas import TTSRequest, TTSResponse, STTRequest, STTResponse, UserCreate, UserRead, MessageCreate, MessageRead, Token
from crud import create_user, get_user_by_email, create_message, get_messages_for_user, authenticate_user, get_all_users, delete_user
from security import create_access_token
from database import SessionLocal, engine
from models import Base, User, Message
from config import settings

database.db.connect()
database.db.create_tables([models.User, models.Item])
database.db.close()

app = FastAPI()
router = APIRouter()

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_tts_client():
    pass


def get_stt_client():
    pass


@app.post("/token", response_model=Token, tags=["authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=UserRead, tags=["Users"])
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@app.post("/tts", response_model=TTSResponse, tags=["TTS"])
async def perform_text_to_speech(tts_request: TTSRequest, tts_client=Depends(get_tts_client)):
    try:
        audio_content = await tts_client.synthesize_speech(text=tts_request.text, voice=tts_request.voice)
        return TTSResponse(audio_content=audio_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stt", response_model=STTResponse, tags=["STT"])
async def perform_speech_to_text(file: UploadFile = File(...), stt_client=Depends(get_stt_client)):
    try:
        text = await stt_client.recognize_speech(audio_file=file.file)
        return STTResponse(text=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/me", response_model=UserRead, tags=["Users"])
async def read_user_me(current_user: User):
    return current_user


@app.get("/messages/", response_model=List[MessageRead], tags=["Chat"])
async def read_messages(current_user: User, db: Session = Depends(get_db) ):
    return get_messages_for_user(db=db, user_id=current_user.id)


@app.post("/messages/", response_model=MessageRead, tags=["Chat"])
async def send_message( current_user: User, message: MessageCreate, db: Session = Depends(get_db)):
    return create_message(db=db, message=message, user_id=current_user.id)

admin_router = APIRouter()


@admin_router.get("/admin/users/", response_model=List[UserRead], tags=["Admin"])
async def read_users(current_user: User, db: Session = Depends(get_db)):
    return get_all_users(db=db)


@admin_router.delete("/admin/users/{user_id}", tags=["Admin"])
async def remove_user(current_user: User, user_id: int, db: Session = Depends(get_db),  ):
    if not delete_user(db=db, user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully."}

app.include_router(router)
app.include_router(admin_router)
