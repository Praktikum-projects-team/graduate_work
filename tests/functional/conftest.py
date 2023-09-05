import pytest
import asyncio

pytest_plugins = (
    'tests.functional.fixtures.user',
    'tests.functional.fixtures.request',
    'tests.functional.fixtures.room'
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
