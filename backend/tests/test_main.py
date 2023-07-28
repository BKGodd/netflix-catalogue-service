import requests
from ..app import schemas
import pytest
from .constants import MOCK_TOTAL_AGG, MOCK_MOVIE_AGG, MOCK_SHOW_AGG


# These should match the .env file in the root directory
APP_HOST="http://localhost"
APP_PORT=5400


@pytest.fixture(scope="module")
def app_url():
    return f"{APP_HOST}:{APP_PORT}"


@pytest.fixture(scope="module")
def app_search_url(app_url):
    return f"{app_url}/api/film/"


@pytest.fixture(scope="module")
def app_aggs_url(app_url):
    return f"{app_url}/api/aggs/"


@pytest.fixture
def check_against_scheme_types():
    def _check_against_scheme_types(data, schema_dict):
        assert isinstance(data, list)
        for result in data:
            assert result.keys() == schema_dict.keys()
            for key, value in schema_dict.items():
                assert type(result[key]) == type(value) or result[key] is None
    return _check_against_scheme_types


def test_connection(app_url):
    assert requests.get(app_url).status_code == 200


def test_wrong_endpoint(app_url):
    assert requests.get(app_url + "/api/").status_code == 404


@pytest.mark.parametrize("film_type", ["movie", "show"])
def test_valid_query(app_search_url, film_type, check_against_scheme_types):
    response = requests.get(f"{app_search_url}{film_type}/", params={"query": "parks"})
    model = schemas.Film().model_dump()
    data = response.json()
    check_against_scheme_types(data, model)
    # It should not return an empty list
    assert data != []
    assert response.status_code == 200


@pytest.mark.parametrize("film_type", ["movie", "show"])
def test_empty_query(app_search_url, film_type):
    response = requests.get(f"{app_search_url}{film_type}/", params={"query": ""})
    data = response.json()
    # It should return an empty list
    assert data == []
    assert response.status_code == 200


@pytest.mark.parametrize("film_type", ["movie", "show"])
def test_wrong_query_param(app_search_url, film_type):
    response = requests.get(f"{app_search_url}{film_type}/", params={"wrong": "parks"})
    assert response.status_code == 422


@pytest.mark.parametrize("film_type", ["movie", "show"])
def test_no_search_matches(app_search_url, film_type):
    response = requests.get(f"{app_search_url}{film_type}/",
                            params={"query": "thiscannotpossiblymatchanything"})
    data = response.json()
    # It should return an empty list
    assert data == []
    assert response.status_code == 200


@pytest.mark.parametrize("agg_type", ["", "movie/", "show/"])
def test_known_aggs(app_aggs_url, agg_type):
    response = requests.get(f"{app_aggs_url}{agg_type}")
    data = response.json()
    print(data)
    if agg_type == "":
        assert data == MOCK_TOTAL_AGG
    elif agg_type == "movie":
        assert data == MOCK_MOVIE_AGG
    elif agg_type == "show":
        assert data == MOCK_SHOW_AGG

    assert response.status_code == 200


@pytest.mark.parametrize("agg_type", ["film", "movies", "shows"])
def test_unknown_agg_endpoint(app_aggs_url, agg_type):
    response = requests.get(f"{app_aggs_url}{agg_type}/")
    assert response.status_code == 404
