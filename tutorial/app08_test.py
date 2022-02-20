from fastapi.testclient import TestClient

from run import app

client = TestClient(app)  # 先 pip install pytest


def test_run_bg_task():  # 函数名用 test_ 开头是 pytest 规范, 注意不是 async def
    response = client.post(url = '/chapter08/background_tasks?framework=FastAPI')
    assert response.status_code == 200
    assert response.json() == {'message': '任务已在后台运行'}


def test_run_bg_task_q():  # 函数名用 test_ 开头是 pytest 规范, 注意不是 async def
    response = client.post(url = '/chapter08/background_tasks?framework=FastAPI?query=1')
    assert response.status_code == 200
    assert response.json() == {'message': '任务已在后台运行'}