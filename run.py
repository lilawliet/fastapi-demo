import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from tutorial import app03, app04, app05, app06, app07, app08

from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='FastAPI Demo ',
    description='FastAPI Demo 新馆病毒疫情跟踪器',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc',
    # dependencies=[Depends(verify_token), Depends(verify_key)]
)


'''
依赖注入：
    * 提高代码复用率
    * 共享数据库连接
    * 增强安全、认证和角色管理
'''


# mount 表示将某个目录下一个独立应用挂载过来， 不会再 API 交互文档中显示
app.mount('/static', app=StaticFiles(directory='./static'), name='static')


@app.exception_handler(StarletteHTTPException)  # 重写 HTTPException 异常处理器
async def http_exception_handler(reqeust, exc):
    '''
    :param request: 请求
    :param exc: 异常
    :return: 返回值
    '''
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    '''
    :param request: 请求
    :param exc: 异常
    :return: 返回值
    '''
    return PlainTextResponse(str(exc), status_code=400)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    processtime = time.time() - start_time
    response.headers['X-Process-Time'] = str(processtime)  # 自定义请求头一般用 X- 开头
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://127.0.0.1',
        'htpp://127.0.0.1:8080',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastAPI依赖注入系统'])
app.include_router(app06, prefix='/chapter06', tags=['第六章 安全、认证和授权'])
app.include_router(app07, prefix='/chapter07', tags=['第七章 数据库操作和目录文件设置'])
app.include_router(app08, prefix='/chapter08', tags=['第八章 中间件、CORS、后台任务、测试用例'])


if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True, debug=True, workers=10)

