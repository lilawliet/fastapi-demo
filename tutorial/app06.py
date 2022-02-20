from faulthandler import disable
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt

app06 = APIRouter()


'''
    OAuth2.0 授权模式
     * 授权码模式
     * 隐式授权模式
     * 密码授权模式
     * 客户端凭证授权模式
'''

''' OAuth2 密码模式和 FastAPI 的 OAuth2PasswordBearer '''

'''
    OAuth2PasswordBearer 是接收url的一个类，客户端会发送 username password 然后得到 token
    OAuth2PasswordBearer 指明客户端获取请求token的地址
    没有认证返回 401 状态码 （UNAUTHORIZED）
'''
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/chapter06/token')  # http://127.0.0.1:8000/chapter06/token

@app06.get('oauth2_password_bearer')
async def oauth2_password_bearer(token: str = Depends(oauth2_schema)):
    return {'token': token}


''' 基于 password 和 Bearer token 的 OAuth2 认证 '''
fake_users_db = {
    'john snow': {
        'username': 'john snow',
        'full_name': 'John Snow',
        'email': '1@qqq.com',
        'hashed_password': 'fakehashedsecret',
        'disabled': False
    },
    'john sayne': {
        'username': 'john sayne',
        'full_name': 'John Sayne',
        'email': '2@qqq.com',
        'hashed_password': 'fakehashedsecret',
        'disabled': True
    },
}


def fake_hash_password(password: str):
    return 'fakehashed' + password


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


@app06.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect user info'
        )
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect user info'
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Disabled User'
        )
    return {'access_token': user.username, 'token_type': 'bearer'}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token: str):
    user = get_user(fake_users_db, token)
    return user


def get_current_user(token: Depends(oauth2_schema)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'}  # OAuth2 规范， 认证失败时返回
        )
    pass


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Inactive User'
        )


''' 基于 JWT （JSON Web Token）验证 '''
fake_users_db = {
    'john snow': {
        'username': 'john snow',
        'full_name': 'John Snow',
        'email': '1@qqq.com',
        'hashed_password': 'fa23346rtgczt4kehasfdghedsesdfsdfgdscret',
        'disabled': False
    },
}

# linux : 生成密钥 openssl rand -hex 32
SECRET_KEY = '356rkjfx8szx9hrjkzcnvm84543h53kjxcu98e4tr'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    ''' 返回给用户的token '''
    access_token: str
    token_type: str

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto') # bcrypt: 加密算法

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/chapter06/jwt/token')

def verify_password(plain_password: str, hashed_password: str):
    ''' 校验密码 '''
    # return pwd_context.verify(plain_password, hashed_password)
    return True

def jwt_get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def jwt_authenticate_user(db, username: str, password: str):
    user = jwt_get_user(db=db, username=username)
    if not user:
        return None
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return None
    return user

def created_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

@app06.post('/jwt/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = jwt_authenticate_user(db=fake_users_db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect user',
            headers={'WWW-Authenticate': 'Bearer'} 
        )
    access_token_expires =timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = created_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires 
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


async def jwt_get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'} 
    )

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user = jwt_get_user(db=fake_users_db, username=username)
        return user
    except:
        raise credentials_exception


async def jwt_get_current_active_user(current_user: User = Depends(jwt_get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Disabled User' )
    return current_user


@app06.get('/jwt/user/me')
async def jwt_user_me(current_user: User = Depends(jwt_get_current_active_user)):
    ''' 依赖注入、嵌套依赖 '''
    return current_user