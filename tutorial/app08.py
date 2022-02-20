from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends

app08 = APIRouter()

''' run.py Middleware 中间件 '''
# 带 yield 的依赖的退出部分代码 和 后台任务 会在中间件之后运行


def bg_task(framework: str):
    with open('README.md', mode='a', encoding='utf-8') as f:
        f.write(f'### {framework} 框架精讲')


@app08.post('/background_tasks')
async def run_bg_task(framework: str, background_task: BackgroundTasks):
    '''
    :param framework: 被调用的后台任务函数的参数
    :param background_task: FastAPI.BackgroundTasks
    :return: 
    '''
    background_task.add_task(bg_task, framework)
    return {'message': '任务已在后台运行'}


def continue_write_readme(background_tasks: BackgroundTasks, query: Optional[str] = None):
    if query:
        background_tasks.add_task(bg_task, '\n> 整体介绍 FastAPI，快速上手开发，结合 API 文档讲解')
    return query


@app08.post('/dependency/background_tasks')
async def denpendency_run_bg_task(query: str = Depends(continue_write_readme)):
    if query:
        return {'message': '任务已经在后台运行'}
    return {'message': '无查询参数'}