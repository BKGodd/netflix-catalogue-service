"""
Created by: Brandon Goddard
Description: This module is for testing the main module,
             which defines the API.
"""
import requests
import pytest
from ..app import schemas
from .constants import MOCK_TOTAL_AGG, MOCK_MOVIE_AGG, MOCK_SHOW_AGG


# These should match the .env file in the root directory
APP_HOST="http://localhost"
APP_PORT=5400
TIMEOUT=10


@pytest.fixture(scope="module")
def app_url():
    """
    A fixture for the base URL of the API.
    
    Returns:
        str: The URL of the API.
    """
    return f"{APP_HOST}:{APP_PORT}"


@pytest.fixture(scope="module")
def app_search_url(app_url):
    """
    A fixture for the search URL of the API.
    
    Returns:
        str: The URL of the search endpoint.
    """
    return f"{app_url}/api/film/"


@pytest.fixture(scope="module")
def app_aggs_url(app_url):
    """
    A fixture for the aggregation URL of the API.
    
    Returns:
        str: The URL of the aggregation endpoint.
    """
    return f"{app_url}/api/aggs/"


@pytest.fixture
def check_against_scheme_types():
    """
    A fixture for comparing the types of the response data.
    
    Returns:
        function: A function for comparing the types of the response data.
    """
    def _check_against_scheme_types(data, schema_dict):
        assert isinstance(data, list)
        for result in data:
            assert result.keys() == schema_dict.keys()
            for key, value in schema_dict.items():
                assert isinstance(result[key], type(value)) or result[key] is None
    return _check_against_scheme_types


def test_connection(app_url):
    """
    Test the connection to the API.
    
    Args:
        app_url (str): The URL of the API.
    
    Returns:
        None
    """
    assert requests.get(app_url, timeout=TIMEOUT).status_code == 200


def test_wrong_endpoint(app_url):
    """
    Test an incorrect endpoint.
    
    Args:
        app_url (str): The URL of the API.
    
    Returns:
        None
    """
    assert requests.get(app_url + "/api/", timeout=TIMEOUT).status_code == 404


@pytest.mark.parametrize("film_type", ["movie", "show"])
def test_valid_query(app_search_url, film_type, check_against_scheme_types):
    """
    Test a set of valid queries for movies and shows.
    
    Args:
        app_search_url (str): The URL of the search endpoint.
        film_type (str): The type of film to retrieve, being 'movie' or 'show'.
        check_against_scheme_types (function): A function for comparing the 
                                                types of the response data.
    
    Returns:
        None
    """
    response = requests.get(f"{app_search_url}{film_type}/",
                            params={"query": "parks"},
                            timeout=TIMEOUT)
    model = schemas.Film().model_dump()
    data = response.json()
    check_against_scheme_types(data, model)
    # It should not return an empty list
    assert data != []
    assert response.status_code == 200


@pytest.mark.parametrize("film_type", ["movie", "show"])
def test_empty_query(app_search_url, film_type):
    """
    Test an empty query for movies and shows.
    
    Args:
        app_search_url (str): The URL of the search endpoint.
        film_type (str): The type of film to retrieve, being 'movie' or 'show'.
    
    Returns:
        None
    """
    response = requests.get(f"{app_search_url}{film_type}/",
                            params={"query": ""},
                            timeout=TIMEOUT)
    data = response.json()
    # It should return an empty list
    assert data == []
    assert response.status_code == 200


@pytest.mark.parametrize("film_type", ["movie", "show"])
def test_wrong_query_param(app_search_url, film_type):
    """
    Test an incorrect query parameter for movies and shows.

    Args:
        app_search_url (str): The URL of the search endpoint.
        film_type (str): The type of film to retrieve, being 'movie' or 'show'.

    Returns:
        None
    """
    response = requests.get(f"{app_search_url}{film_type}/",
                            params={"wrong": "parks"},
                            timeout=TIMEOUT)
    assert response.status_code == 422


@pytest.mark.parametrize("film_type", ["movie", "show"])
def test_no_search_matches(app_search_url, film_type):
    """
    Test a query that should not match any documents in the database for movies and shows.

    Args:
        app_search_url (str): The URL of the search endpoint.
        film_type (str): The type of film to retrieve, being 'movie' or 'show'.

    Returns:
        None
    """
    response = requests.get(f"{app_search_url}{film_type}/",
                            params={"query": "thiscannotpossiblymatchanything"},
                            timeout=TIMEOUT)
    data = response.json()
    # It should return an empty list
    assert data == []
    assert response.status_code == 200


@pytest.mark.parametrize("agg_type", ["", "movie/", "show/"])
def test_known_aggs(app_aggs_url, agg_type):
    """
    Test whether the aggregation endpoint returns the correct data.

    Args:
        app_aggs_url (str): The URL of the aggregation endpoint.
        agg_type (str): The type of aggregation to retrieve, being 'movie' or 'show'.

    Returns:
        None    
    """
    response = requests.get(f"{app_aggs_url}{agg_type}", timeout=TIMEOUT)
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
    """
    Test an incorrect aggregation endpoint.

    Args:
        app_aggs_url (str): The URL of the aggregation endpoint.
        agg_type (str): The type of aggregation to retrieve, being 'movie' or 'show'.

    Returns:
        None
    """
    response = requests.get(f"{app_aggs_url}{agg_type}/", timeout=TIMEOUT)
    assert response.status_code == 404
