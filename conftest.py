import logging
from typing import Any, AsyncGenerator, Dict, Tuple

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config import get_config
from main import app
from scripts.reset_database import main as run_seed_script

pytest_plugins = ("pytest_asyncio",)

_test_failed_incremental: Dict[str, Dict[Tuple[int, ...], str]] = {}


def pytest_runtest_makereport(item: Any, call: Any) -> None:
    if "incremental" in item.keywords:
        # incremental marker is used
        if call.excinfo is not None:
            # the test has failed
            # retrieve the class name of the test
            cls_name = str(item.cls)
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the test function
            test_name = item.originalname or item.name
            # store in _test_failed_incremental the original name of the failed test
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                parametrize_index, test_name
            )


def pytest_runtest_setup(item: Any) -> None:
    if "incremental" in item.keywords:
        # retrieve the class name of the test
        cls_name = str(item.cls)
        # check if a previous test has failed for this class
        if cls_name in _test_failed_incremental:
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the first test function to fail for this class name and index
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # if name found, test has failed for the combination of class name & test name
            if test_name is not None:
                pytest.xfail("previous test failed ({})".format(test_name))


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator:
    # logging.getLogger("httpx").setLevel("CRITICAL")
    # logging.getLogger("httpx").propagate = False
    async with LifespanManager(app=app) as manager:
        env = get_config()
        if env.ENVIRONMENT != "testing":
            raise Exception("Set environment to testing")

        mongo_client: AsyncIOMotorClient = app.state.mongo_client
        # This block of code clean the database before runing the tests

        logging.warning("Cleaning testing database")

        await run_seed_script(
            mongo_client=mongo_client, database_name=env.TESTING_DATABASE_NAME
        )
        async with AsyncClient(
            app=manager.app,
            base_url="http://localhost:8000",
        ) as client:
            logging.info("Client is ready")
            yield client
