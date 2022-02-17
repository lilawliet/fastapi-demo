import imp
from pydantic import BaseModel, ValidationError, constr
from datetime import date, datetime
from typing import List, Optional
from pathlib import Path

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base


class User(BaseModel):
    id: int  # 必填
    name: str = 'Josn Snow'  # 有默认值，选填
    signup_ts: Optional[datetime] = None  # 利用 Optional 可变为选填
    friends: List[int] = []

external_dat = {
    'id': '123',
    'signup_ts': '2022-12-12 12:12',
    'friends': [1, 2, '3']
}

user = User(**external_dat)
print(user.id)
print(repr(user.signup_ts))  # repr() 函数将对象转化为供解释器读取的形式。
print(user.dict())
print(User.parse_obj(obj=external_dat))
print(User.parse_raw('{"id":"123","signup_ts":"2022-12-12 12:12","friends": [1, 2, 3]}'))

path = Path('pydantic_tutorial.json')
path.write_text('{"id":"123","signup_ts":"2022-12-12 12:12","friends": [1, 2, 3]}')
print(User.parse_file(path))

print(user.schema())
print(user.schema_json())
print(user.construct(external_dat))  # 不做校验

print(user.__fields__.keys())  # 字段注明类型，顺序就不会乱

print('-------------- 校验 ---------------------')
try:
    User(id=1, signup_ts=datetime.today(), friends=[1,2,'sdf'])
except ValidationError as e:
    print(e.json())

print('\033[31m4. --- 递归模型 ---\033[0m')

class Sound(BaseModel):
    sound: str

class Dog(BaseModel):
    birthday: date
    weight: float = Optional[None]
    sound: List[Sound]

dogs = Dog(birthday=date.today(), weight=6.6, sound=[{"sound": "wang"}, {"sound": "wa"}])
print(dogs.dict())

print('-------------- orm ---------------------')

Base = declarative_base()

class CompanyOrm(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(64), unique=True)
    domains = Column(ARRAY(String(255)))

class CompanyMode(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=64)
    domains: List[constr(max_length=255)]

    class Config:
        orm_mode = True

co_orm = CompanyOrm(
    id = 234,
    public_key = 'foobar',
    name = 'Testing',
    domains = ['example.com', 'imooc.com']
)

print(CompanyMode.from_orm(co_orm))