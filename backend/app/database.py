import os
import csv
from ssl import create_default_context
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from datetime import datetime
from schemas import ELASTIC_MAP, RATING_TO_ID


def get_elastic_db():
    """
    Establish and return a connection from a pool of Elasticsearch database instances.

    Returns:
        (AsyncElasticsearch): Database connection instance.
    """
    context = create_default_context(cafile=os.environ['ESDB_CERT'])
    esdb = AsyncElasticsearch(hosts=f"https://esdb:{os.environ['ELASTIC_PORT']}",
                            basic_auth=(os.environ['ELASTIC_USERNAME'],
                                        os.environ['ELASTIC_PASSWORD']),
                            ssl_context=context)

    return esdb


async def init_elastic_db(esdb):
    """Initialize Elasticsearch database on service startup."""
    # Create elasticsearch index if DNE
    if not await esdb.indices.exists(index=os.environ['ELASTIC_INDEX']):
        # Explicit mappings
        await esdb.indices.create(index=os.environ['ELASTIC_INDEX'], mappings=ELASTIC_MAP)

    # If no data is in the index, load in the CSV file
    num_docs = await esdb.count(index=os.environ['ELASTIC_INDEX'])
    if num_docs['count'] == 0:
        await async_bulk(esdb, get_row('datasets/netflix.csv'))

