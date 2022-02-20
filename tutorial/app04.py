from typing import Optional, List, Union
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel, EmailStr

app04 = APIRouter()

class User(BaseModel):
    username: str
    email: EmailStr
    mobile: str = '10086'
    address: str = None
    full_name: Optional[str] = None

class UserIn(User):
    password: str

class UserOut(User):
    pass

users = {
    'user01': {
        'username': 'str',
        'email': '1@c.com',
        'address': 'str = None',
        'full_name': 'Optional[str] = None'
    },
    'user02': {
        'username': 'str2',
        'email': '2@c.com',
        'mobile': '11',
        'address': 'str = None',
        'full_name': 'Optional[str] = None'
    }
}

# path operation
# response_model_exclude_unset True 默认值不包含在响应中返回
@app04.post('/response_model', response_model=UserOut, response_model_exclude_unset=True)
async def response_mdoel(user: UserIn):
    print(user.password)
    return users['user01']


@app04.post(
    '/response_model/attributes',
    # response_model=Union[UserIn, UserOut]
    # response_model=List[]
    # response_model_include=[]  # 包含某些字段
    # response_model_exclude=[]  # 排除某些字段
)
async def response_model_attributes(user: UserIn):
    return user


@app04.post('/status_code', status_code=200)
async def status_code():
    return {'status_code': 200}


@app04.post('/status_code_ok', status_code=status.HTTP_200_OK)
async def status_code():
    return {'status_code': status.HTTP_200_OK}


''' Form Data '''
@app04.post('/login')
async def login(username: str=Form(...), password: str=Form(...)):
    return {'username': username}


@app04.post('/file')
async def file_1(
    file: Optional[bytes]=File(None),
    files: List[bytes]=File(...)
):
    return {'file_size': len(file)}


@app04.post('/upload_files')
async def upload_files(files: List[UploadFile]=File(...)):  # 上传大文件 uploadfile
    '''
    UploadFile 优势
    1. 文件存储在内存中，达到内存阈值后，被保存在磁盘中
    2. 使用图片、视频
    3. 可以获得元数据，如文件名，创建时间
    4. 异步接口
    5. 上传文件的python文件对象，可操作如：write()、 read()、 seek()、 close()
    '''
    for file in files:
        contents = await file.read()
        print(contents)
    return {}

    
""" Path Operation Configuration 路径操作配置 """
@app04.post(
    '/path_operation',
    response_model=UserOut,
    # tags=['Path', 'Operation', 'Configuration'],
    description='This is description',
    response_description='This is response_description',
    # deprecated=True, # 废弃
    status_code=status.HTTP_200_OK
)
async def path_operation_configuration(user: UserIn):
    '''
    Path Operation Configuration 路径操作配置
    :param user: 用户信息
    :return: 返回值
    '''
    return user.dict()


''' Handing Errors 错误处理 '''
@app04.get('/http_exception')
async def http_exception(city: str):
    if city != 'Beijing':
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='City not found', 
            headers={'X-Error': 'Error'
        })
    return {'city': city}


@app04.get('/http_exception/{city_id}')
async def override_http_exception(city_id: int):
    if city_id == 1:
        raise HTTPException(
            status_code=418, 
            detail='City not found', 
            headers={'X-Error': 'Error'
        })
    return {'city_id': city_id}