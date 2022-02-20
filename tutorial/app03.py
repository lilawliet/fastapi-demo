from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import APIRouter, Cookie, Header, Path, Query


app03 = APIRouter()


@app03.get('/path/{parameters}')
def path_params01(parameters: str):
    return {'message': parameters}


class CityName(str, Enum):
    Beijing = "Beijing China"
    Shanghai = "shanghai China"


@app03.get('/emun/{city}')
async def latest(city: CityName):
    if city == CityName.Shanghai:
        return {'city_name': city, 'confirmed': 122, 'death': 0}
    if city == CityName.Beijing:
        return {'city_name': city, 'confirmed': 12, 'death': 0}
    return {'city_name': city, 'confirmed': 'unknown'}


@app03.get('/file/{file_path:path}')
def filepath(file_path: str):
    return f'The file path is {file_path}'


@app03.get('/path/{num}')
def path_params_validate(
    num: int = Path(..., title='your nunber', description='不可描述', ge=1, le=10)
):
    return {}


@app03.get('/query')
def page_limit(page: int=1, limit: Optional[int]=None):
    if limit:
        return {'page': page, 'limit': limit}
    return {'page': page}


@app03.get('/query/bool/conversion')
def type_conversion(param: bool=False):
    # bool类型转换 yes on 1 True true 会转换成 ture
    return param


@app03.get('/query/validations')
def query_params_validate(
    value: str = Query(..., min_length=8, max_length=16, regex='^a'),
    values: List[str] = Query(default=['v1', 'v2'], alias='alias_name')
):
    return value, values


'''
 Request Body and Fields 请求体和字段
'''
class CityInfo(BaseModel):
    name: str = Field(..., example='Beijing')  # exanple 示例
    country: str
    country_code: str = None
    country_population: int = Field(default=800, title='人口数量', description='国家人口数量', ge=800)

    class Config:
        scheme_extra = {
            'example': {
                'name': 'Shanghai',
                'country': 'China',
                'country_code': 'CN',
                'country_population': 1400000000
            }
        }

@app03.post('/request_body/city')
def city_info(city: CityInfo):
    print(city.name, city.country)
    return city.dict()


@app03.put('/request_body/city/{name}')
def mix_city_info(
    name: str,
    city01: CityInfo,
    city02: CityInfo,  # body 可以定义多个
    confirmed: int = Query(ge=0, description='确诊数', default=0),
    death: int = Query(ge=0, description='死亡数', default=0)
):
    if name == 'Shanghai':
        return {'Shanghai': {'confirmed': confirmed, 'death': death}}
    return city01.dict(), city02.dict()


''' 数据格式嵌套 '''
class Data(BaseModel):
    city: List[CityInfo] = None  # 数据格式嵌套
    date: datetime
    confirmed: int = Field(ge=0, description='确诊数', default=0)
    death: int = Field(ge=0, description='死亡数', default=0)
    recovered: int = Field(ge=0, description='痊愈', default=0)

@app03.put('/request_body/nested')
def nested_models(data: Data):
    return data


@app03.get('/cookie')
def cookie(cookie_id: Optional[str] = Cookie(None)):  # 定义Cookie参数要使用Cookie类
    return {'cookie_id': cookie_id}


@app03.get('/header')
def header(
    user_agent: Optional[str] = Header(None, convert_underscores=True),
    x_token: List[str] = Header(None)
):  # convert_underscores 是否转换下划线
    '''
    有些浏览器不支持请求头带有下划线

    '''
    return {'User-Agent': user_agent, 'x_token': x_token}