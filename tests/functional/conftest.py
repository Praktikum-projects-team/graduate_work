import pytest
import asyncio


pytest_plugins = ('tests.functional.fixtures.request', 'tests.functional.fixtures.user')


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
