from fastapi.testclient import TestClient

from main import app


# TestClient 是 FastAPI 提供的测试客户端。
# 它可以在不真正启动服务器的情况下，直接请求我们的接口。
client = TestClient(app)


def test_read_root_status_code():
    """测试 / 路由是否能正常返回 200 状态码。"""
    response = client.get("/")
    assert response.status_code == 200
