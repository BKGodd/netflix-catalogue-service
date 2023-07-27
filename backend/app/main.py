from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError
from elasticsearch import AsyncElasticsearch
from string import punctuation
from unidecode import unidecode as ud
import os
from collections import ChainMap

import schemas
from database import get_elastic_db, init_elastic_db

app = FastAPI(openapi_url="/api/docs/openapi.json",
              docs_url="/api/docs/")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://nginx:80'], # Where the frontend is hosted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set Elasticsearch dependency
async def get_db():
    esdb = get_elastic_db()
    try:
        yield esdb
    finally:
        await esdb.close()

esdb = get_elastic_db()

@app.on_event("startup")
async def startup():
    """"""
    #esdb = await get_db().__anext__()
    await init_elastic_db(esdb)

@app.on_event("shutdown")
async def shutdown():
    """"""
    #await esdb.close()


@app.get("/api/film/{film_type}/", response_model=schemas.Film)
async def get_film(film_type: str, query: str):
    query = build_query(film_type, query)
    result = await esdb.search(index=os.environ['ELASTIC_INDEX'], query=query,
                               size=1, track_total_hits=True)
    response = result['hits']['hits'][0]['_source']
    response.pop('type')
    response['rating'] = schemas.ID_TO_RATING[response['rating']]

    return response


@app.get("/api/aggs/movie/", response_model=schemas.MovieAggs)
async def get_movie_aggs():
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


def simplify_text(text):
    """
    Process the given text to be either queried or inserted into
    the Elasticsearch database.

    Args:
        text (str): The text to process and simplify for use.

    Returns:
        (str): The text after being processed.

    Notes:
        The following changes are made to the string:
            - Punctuation removed
            - Character accents removed
            - All extraneous whitespace removed
            - Lowered capitalization
    """
    if isinstance(text, str):
        text = ud(text.translate(str.maketrans('', '', punctuation)))
        return ' '.join(text.split()).lower()
    return ''


def build_query(selector, search_text=''):
    """
    Create a custom-formatted query dictionary to be used for the
    Elasticsearch database, based on the query texts provided.

    Args:
        inputs (tuple): The query texts provided by the user
                        from the GET request, being 'title'
                        and 'location'.

    Returns:
        (dict): The ingestible query request needed for
                performing a search on Elasticsearch.
        (dict): The ingestible aggreagation request needed for
                performing aggregation calculations
                on Elasticsearch.
    """
    search_param = -1
    if selector == 'movie':
        search_param = 1
    elif selector == "show":
        search_param = 0

    #if selector == 'actor':
    #    search_fields = ['cast']
    #if selector == 'director':
    #    search_fields = ['director']
    #else:
        #search_fields = ['title', 'director', 'cast', 'country',
        #                 'genres', 'description']
        
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


def build_aggs(avg_duration=False, histo_duration=False, directors=False,
               actors=False, genres=False, countries=False, ratings=False):
    """
    """
    aggs = {
        "total_agg": {"value_count": {"field": "type"}}
    }

    if avg_duration:
        aggs["avg_dur_agg"] = {"avg": {"field": "duration"}}
    if histo_duration:
        aggs["histo_dur_agg"] = {"histogram": {"field": "duration",
                                               "interval": 20,
                                               "min_doc_count": 10}}
    if directors:
        aggs["director_agg"] = {"terms": {"field": "director",
                                          "size": 5}}
    if actors:
        aggs["actor_agg"] = { "terms": {"field": "cast",
                                        "size": 5}}
    if genres:
        aggs["genre_agg"] = { "terms": {"field": "genres",
                                           "size": 5}}
    if countries:
        aggs["country_agg"] = {"terms": {"field": "country",
                                         "size": 5}}
    if ratings:
        aggs["rating_agg"] = {"terms": {"field": "rating",
                                        "size": 5}}

    return aggs
