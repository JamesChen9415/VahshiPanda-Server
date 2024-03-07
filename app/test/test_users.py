import pytest
from httpx import AsyncClient

from ..app import app

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_root():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:5000") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Bigger Applications!"}


# @pytest.mark.parametrize("anyio_backend", ["asyncio"])
# @pytest.mark.parametrize(
#     "data,expected_status_code, expected_resp",
#     [
#         (
#             {
#                 "username": "bob",
#                 "email": "bob.chen@example.com",
#                 "password": "password123",
#             },
#             200,
#             {
#                 # "id": 2,
#                 "username": "bob",
#                 "email": "bob.chen@example.com",
#                 "is_active": True,
#                 # "is_locked": False,
#             },
#         ),
#         # (
#         #     "second test post",
#         #     "lorem ipsum dummy content",
#         # ),
#         # (
#         #     "third test post",
#         #     "lorem ipsum dummy content",
#         # ),
#     ],
# )
# async def test_register_user(data, expected_status_code, expected_resp):
#     """
#     Test http://127.0.0.1:5000/users/register endpoint
#     """
#     async with AsyncClient(app=app, base_url="http://127.0.0.1:5000") as ac:
#         response = await ac.post("/users/register", json=data)

#     assert response.status_code == expected_status_code

#     actual_resp = response.json()
#     del actual_resp["id"]  # ignore id
#     assert actual_resp == expected_resp


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
@pytest.mark.parametrize(
    "data,expected_status_code, expected_resp",
    [
        (
            {
                "username": "alice",
                "email": "alice.chen@example.com",
                "password": "password123",
                "grant_type": "password",
            },
            200,
            {
                "token_type": "bearer",
            },
        ),
    ],
)
async def test_login_for_access_token(data, expected_status_code, expected_resp):
    """
    Test http://127.0.0.1:5000/users/token endpoint
    """
    async with AsyncClient(app=app, base_url="http://127.0.0.1:5000") as ac:
        response = await ac.post(
            "/users/token",
            data=data,
            headers={"content-type": "application/x-www-form-urlencoded"},
        )

    assert response.status_code == expected_status_code

    actual_resp = response.json()
    del actual_resp["access_token"]  # ignore access_token
    assert actual_resp == expected_resp
