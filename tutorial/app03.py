from enum import Enum
from fastapi import APIRouter, Path

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