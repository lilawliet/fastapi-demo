import imp
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class CityInfo(BaseModel):
    province: str
    country: str
    is_affected: Optional[bool] = None

# async 异步方式
@app.get('/')
async def hello_world():
    return {'hellow': 'world'}

@app.get('/city/{city}')
async def result(city: str, query_string: Optional[str] = None):
    return {'city': city, 'query_string': query_string}

@app.put('/city/{city}')
async def result(city: str, city_info: CityInfo):
    return {'city': city, 'country': city_info.country, 'is_affected': city_info.is_affected}


# uvicorn hello_world:app --reload