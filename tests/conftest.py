from uuid import uuid4

import pytest

from .fixtures import *


def pytest_config(config):
    pytest.user_uuid = uuid4()
    pytest.member_uuid = uuid4()
