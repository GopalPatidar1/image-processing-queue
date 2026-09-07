from httpx import AsyncClient, ASGITransport
from app.main import app
import pytest_asyncio

@pytest_asyncio.fixture(scope="session")
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        follow_redirects=True
    ) as client:
        yield client