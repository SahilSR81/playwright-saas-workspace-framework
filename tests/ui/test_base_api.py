import pytest

from api.base_api import BaseAPI


@pytest.mark.api
def test_api_session_created():

    api = BaseAPI()

    assert api.session is not None

    api.close()


@pytest.mark.api
def test_default_headers():

    api = BaseAPI()

    assert "application/json" in api.session.headers["Accept"]

    api.close()


@pytest.mark.api
def test_base_url():

    api = BaseAPI()

    assert api.base_url.startswith("https://")

    api.close()


@pytest.mark.api
def test_api_session_close():

    api = BaseAPI()

    api.close()

    assert True