from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional

app05 = APIRouter()


async def common_parameters(
    query: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    return {'query': query, 'page': page, 'limit': limit}


@app05.get('/dependency01')
async def dependency01(commons: dict = Depends(common_parameters)):
    return {}


@app05.get('/dependency02')
def dependency02(commons: dict = Depends(common_parameters)):  # 同步异步皆可调用
    return {} 


fake_items_db = [
    {'item_name', 'Foo'},
    {'item_name', 'Bar'},
    {'item_name', 'Baz'}
]

class CommonQueryParams:
    def __init__(self, query: Optional[str] = None, page: int = 1, limit: int = 10) -> None:  # -> None 表示返回 None
        self.query = query
        self.page = page
        self.limit = limit


@app05.get('/classes_as_dependencies')
# async def classes_as_dependencies(commons: CommonQueryParams = Depends(CommonQueryParams)):
# async def classes_as_dependencies(commons: CommonQueryParams = Depends()):
async def classes_as_dependencies(commons  = Depends(CommonQueryParams)):
    response = {}
    if commons.query:
        response.update({'query': commons.query})
    items = fake_items_db[commons.page: commons.page + commons.limit]
    response.update({'items': items})
    return response


''' Sub-dependencies 子依赖 '''
def query(query: Optional[str] = None):
    return {'query': query}


def sub_query(query: str = Depends(query), last_query: Optional[str] = None):
    if not query:
        return last_query
    return query


@app05.get('/sub_dependency')
async def sub_dependency(final_query: str = Depends(sub_query, use_cache=True)):
    ''' use_cache 默认是True , 表示当多个依赖共有一个子依赖时，每次request请求只会调用一次子依赖'''
    return {'sub_dependency': final_query}


''' Dependencies in path operation decorators 路径操作装饰器中的多依赖 '''
async def verify_token(x_token: str = Header(...)):
    if x_token != 'fake-super-secret-token':
        raise HTTPException(status_code=400, detail='X-Token header invalid')
    return x_token


async def verify_key(x_key: str = Header(...)):
    if x_key != 'fake-super-secret-token':
        raise HTTPException(status_code=400, detail='X-Key header invalid')
    return x_key


''' 路径操作装饰器中的多依赖 '''
@app05.get('/dependency_in_path_operation', dependencies=[Depends(verify_token), Depends(verify_key)])
async def dependency_in_path_operation():
    return [{'user': 'user1'}, {'user': 'user2'}]


''' Global Dependencies 全局依赖 '''
app05 = APIRouter(dependencies=[Depends(verify_token), Depends(verify_key)])


''' 
    使用 yield 关键字依赖 3.7 以上版本 
    常用获取数据库连接，结束后关闭
    3.6 需要 pip install async-exit-stack async-generator
'''
async def get_db():
    db = 'db_connection'
    try:
        yield db
    finally:
        db.endswith('db_close')  # 伪代码
    
async def dependency_a():
    dep_a = 'generate_dep_a()'
    try:
        yield dep_a
    finally:
        dep_a.endswith('db_close')

async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = 'generate_dep_b()'
    try:
        yield dep_b
    finally:
        dep_b.endswith(dep_a)

async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = 'generate_dep_c()'
    try:
        yield dep_c
    finally:
        dep_c.endswith(dep_b)