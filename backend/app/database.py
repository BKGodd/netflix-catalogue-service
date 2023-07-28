"""
Created by: Brandon Goddard
Description: This module is for initializing and loading 
             data into the Elasticsearch database.
"""
import os
import csv
from datetime import datetime
from string import punctuation
from ssl import create_default_context
from unidecode import unidecode as ud
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
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
    """
    Initialize the Elasticsearch database with the
    given connection instance.
    
    Args:
        esdb (AsyncElasticsearch): Database connection instance.
        
    Returns:
        None
    """
    # Create elasticsearch index if DNE
    if not await esdb.indices.exists(index=os.environ['ELASTIC_INDEX']):
        # Explicit mappings
        await esdb.indices.create(index=os.environ['ELASTIC_INDEX'], mappings=ELASTIC_MAP)

    # If no data is in the index, load in the CSV file
    num_docs = await esdb.count(index=os.environ['ELASTIC_INDEX'])
    if num_docs['count'] == 0:
        await async_bulk(esdb, get_row('datasets/netflix.csv'))


def filter_row(row):
    """
    Process the given row to be inserted into the
    Elasticsearch database.

    Args:
        row (dict): The row to process and simplify for use.
    
    Returns:
        None
    """
    # Cleanup unnecessary characters in type
    if row['type'] == 'TV Show':
        row['type'] = 0
    elif row['type'] == 'Movie':
        row['type'] = 1
    else:
        row['type'] = -1

    # Some ratings are incorrectly durations
    if row['rating'] in RATING_TO_ID:
        row['rating'] = RATING_TO_ID[row['rating']]
    else:
        row['rating'] = -1

    # Convert durations to ints for aggregation processing
    if row['duration']:
        new_str = row['duration'].replace('min', '')
        new_str = new_str.replace('Seasons', '').replace('Season', '').strip()
        # Some movies might be listed incorrectly as seasons
        if row['type'] == 1 and int(new_str) < 5:
            row['duration'] = None
        else:
            row['duration'] = int(new_str)


def filter_strings(row):
    """
    Process the given row's strings to be inserted into the
    Elasticsearch database.

    Args:
        row (dict): The row to process and simplify for use.

    Returns:
        None
    """
    # Titles and descriptions could contain punctuation, keep them
    if row['title']:
        row['title'] = filter_text(row['title'], punct=False)
    if row['description']:
        row['description'] = filter_text(row['description'], punct=False)

    # We don't want director names to have punctuation or accents
    if row['director']:
        row['director'] = filter_text(row['director'])

    # Convert cast to a list of names
    if row['cast']:
        row['cast'] = [filter_text(name, punct=False) for name in row['cast'].split(',')]

    # Convert catagories to a list of discrete genres
    if row['genres']:
        row['genres'] = [filter_text(genre) for genre in row['genres'].split(',')]


def filter_dates(row):
    """
    Process the given row's dates to be inserted into the
    Elasticsearch database.

    Args:
        row (dict): The row to process and simplify for use.

    Returns:
        None
    """
    # Reformat date
    if row['date_added']:
        try:
            date = datetime.strptime(row['date_added'].strip(), "%B %d, %Y")
            row['date_added'] = date.strftime("%m%d%Y")
        except ValueError:
            row['date_added'] = None
    else:
        row['date_added'] = None

    # Release year can be converted to int
    if row['release_year']:
        row['release_year'] = int(row['release_year'])



def get_row(csv_filepath):
    """
    Given a CSV filepath, process all rows for
    insertion into the Elasticsearch database.

    Args:
        excel_sheet (Worksheet): Object for accessing excel file data.

    Returns:
        None
    """
    with open(csv_filepath, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            row['genres'] = row.pop('listed_in')
            # For optimizing elasticsearch, turn empty strings to None
            for key, value in row.items():
                if not value:
                    row[key] = None
            # Perform more filtering on specific columns
            filter_dates(row)
            filter_strings(row)
            filter_row(row)
            yield {
                "_id": row.pop('show_id'),
                "_index": os.environ['ELASTIC_INDEX'],
                "_source": row
            }


def filter_text(text, accents=True, punct=True):
    """
    Process the given text to be inserted into the
    Elasticsearch database.

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
        if punct:
            text = text.translate(str.maketrans('', '', punctuation))
        if accents:
            text = ud(text)
        return ' '.join(text.split())
    return ''
