import pytest
from tortoise.contrib.test import finalizer, initializer


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    initializer(["src.models"], app_label="models")
    request.addfinalizer(finalizer)
