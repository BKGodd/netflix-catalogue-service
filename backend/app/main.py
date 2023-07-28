"""
Created by: Brandon Goddard
Description: This module is for defining the API and
             handling requests to the Elasticsearch database.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import schemas
from database import get_elastic_db, init_elastic_db


app = FastAPI(openapi_url="/api/docs/openapi.json",
              docs_url="/api/docs/")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://nginx:80'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a connection from a pool of Elasticsearch database instances
esdb = get_elastic_db()


@app.on_event("startup")
async def startup():
    """
    Initialize the Elasticsearch database on startup.
    
    Returns:
        None
    """
    await init_elastic_db(esdb)


@app.on_event("shutdown")
async def shutdown():
    """
    Close the Elasticsearch database connection on shutdown.

    Returns:
        None
    """
    await esdb.close()


@app.get("/api/film/{film_type}/", response_model=list[schemas.Film])
async def get_film(film_type: str, query: str):
    """
    API endpoint for retrieving a film from the Elasticsearch database.

    Args:
        film_type (str): The type of film to retrieve, being 'movie' or 'show'.
        query (str): The query text to search for in the database.

    Returns:
        (dict): The film data retrieved from the database.
    """
    query = build_query(film_type, query)
    result = await esdb.search(index=os.environ['ELASTIC_INDEX'], query=query,
                               size=8, track_total_hits=True)
    response = []
    # If we get no results back, return an empty model
    if result['hits']['total']['value'] == 0:
        return response
    for hit in result['hits']['hits']:
        hit['_source']['rating'] = schemas.ID_TO_RATING[hit['_source']['rating']]
        hit['_source'].pop('type')
        response.append(hit['_source'])

    return response


@app.get("/api/aggs/movie/", response_model=schemas.MovieAggs)
async def get_movie_aggs():
    """
    API endpoint for retrieving movie aggregations from the Elasticsearch database.
    
    Returns:
        (dict): The movie aggregation data retrieved from the database.
    """
    response = {}
    query = {"term": {"type": 1}}
    aggs = build_aggs(avg_duration=True, histo_duration=True)
    result = await esdb.search(index=os.environ['ELASTIC_INDEX'], query=query,
                                aggs=aggs, size=0, track_total_hits=True)
    # Process the average aggregation
    response['avg_dur_agg'] = int(result['aggregations']['avg_dur_agg']['value'])
    # Process the total aggregation
    response['total_agg'] = result['aggregations']['total_agg']['value']
    # Process the histogram aggregation
    response['histo_dur_agg'] = {}
    for data in result['aggregations']['histo_dur_agg']['buckets']:
        response['histo_dur_agg'][str(int(data["key"]))] = data["doc_count"]

    return response


@app.get("/api/aggs/show/", response_model=schemas.ShowAggs)
async def get_show_aggs():
    """
    API endpoint for retrieving show aggregations from the Elasticsearch database.
    
    Returns:
        (dict): The show aggregation data retrieved from the database.
    """
    response = {}
    query = {"term": {"type": 0}}
    aggs = build_aggs()
    result = await esdb.search(index=os.environ['ELASTIC_INDEX'], query=query,
                                aggs=aggs, size=0, track_total_hits=True)
    # Process the total aggregation
    response['total_agg'] = result['aggregations']['total_agg']['value']

    return response


@app.get("/api/aggs/", response_model=schemas.AllAggs)
async def get_all_aggs():
    """
    API endpoint for retrieving all aggregations from the Elasticsearch database.
    
    Returns:
        (dict): The total aggregation data retrieved from the database.
    """
    response = {}
    query = {"match_all": {}}
    aggs = build_aggs(directors=True, actors=True, genres=True,
                      countries=True, ratings=True)
    result = await esdb.search(index=os.environ['ELASTIC_INDEX'], query=query,
                                aggs=aggs, size=0, track_total_hits=True)
    # Process the total aggregation
    response['total_agg'] = result['aggregations']['total_agg']['value']
    # Process the top aggregations
    top_aggs = ['director_agg', 'actor_agg', 'rating_agg',
                'country_agg', 'genre_agg']
    for agg in top_aggs:
        response[agg] = {}
        for data in result['aggregations'][agg]['buckets']:
            if agg == 'rating_agg':
                key = schemas.ID_TO_RATING[data["key"]]
            else:
                key = data["key"]
            response[agg][key] = data["doc_count"]

    return response


def build_query(selector, search_text=''):
    """
    A helper function for building the Elasticsearch query.

    Args:
        selector (str): The type of film to retrieve, being 'movie' or 'show'.
        search_text (str): The query text to search for in the database.

    Returns:
        (dict): The Elasticsearch query.
    """
    # To optimize ES space, store as a byte
    search_param = -1
    if selector == 'movie':
        search_param = 1
    elif selector == "show":
        search_param = 0

    # Build the final query
    if search_param == -1:
        query = {"match_all": {}}
    else:
        if not search_text:
            query = {"match_none": {}}
        else:
            search_fields = ['title', 'director', 'cast', 'country',
                            'genres', 'description']
            query = {
                "bool": {
                    "must": [
                        {"term": {"type": search_param}},
                        {"multi_match": {"query": search_text,
                                        "fields": search_fields,
                                        "operator": "and"}}
                    ],
                    "minimum_should_match": "100%"
                }
            }

    return query


def build_aggs(**kwargs):
    """
    A helper function for building the Elasticsearch aggregations query.

    Args:
        avg_duration (bool): Whether to include the average duration aggregation.
        histo_duration (bool): Whether to include the histogram duration aggregation.
        directors (bool): Whether to include the director aggregation.
        actors (bool): Whether to include the actor aggregation.
        genres (bool): Whether to include the genre aggregation.
        countries (bool): Whether to include the country aggregation.
        ratings (bool): Whether to include the rating aggregation.
        
    Returns:
        (dict): The Elasticsearch aggregations query.
    """
    # Always return the total aggregation
    aggs = {
        "total_agg": {"value_count": {"field": "type"}}
    }

    if kwargs.get("avg_duration", False):
        aggs["avg_dur_agg"] = {"avg": {"field": "duration"}}
    if kwargs.get("histo_duration", False):
        aggs["histo_dur_agg"] = {"histogram": {"field": "duration",
                                               "interval": 20,
                                               "min_doc_count": 10}}
    if kwargs.get("directors", False):
        aggs["director_agg"] = {"terms": {"field": "director",
                                          "size": 5}}
    if kwargs.get("actors", False):
        aggs["actor_agg"] = { "terms": {"field": "cast.raw",
                                        "size": 5}}
    if kwargs.get("genres", False):
        aggs["genre_agg"] = { "terms": {"field": "genres.raw",
                                           "size": 5}}
    if kwargs.get("countries", False):
        aggs["country_agg"] = {"terms": {"field": "country",
                                         "size": 5}}
    if kwargs.get("ratings", False):
        aggs["rating_agg"] = {"terms": {"field": "rating",
                                        "size": 5}}

    return aggs
