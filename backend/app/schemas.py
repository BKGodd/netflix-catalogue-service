from pydantic import BaseModel


# Aggregation models
class TopAggs(BaseModel):
    """
    API aggregation model for validation.
    
    Attriubutes:
        director_agg (dict[str, int]): The directors with most produced films.
        actor_agg (dict[str, int]): The most active actors in movies and shows.
        rating_agg (dict[str, int]): The most common movie and show ratings.
        country_agg (dict[str, int]): The top countries where films are produced.
        genre_agg (dict[str, int]): The most common genres of movies and shows.
    """
    director_agg: dict[str, int]
    actor_agg: dict[str, int]
    rating_agg: dict[str, int]
    country_agg: dict[str, int]
    genre_agg: dict[str, int]

class TotalAggs(BaseModel):
    """
    API aggregation model for validation.

    Attriubutes:
        total_agg (int): The total number of movies and shows.
    """
    total_agg: int

class DurationAggs(BaseModel):
    """
    API aggregation model for validation.
    
    Attriubutes:
        histo_dur_agg (dict[str, int]): The histogram of durations.
        avg_dur_agg (int): The average duration of the movie or show.
    """
    histo_dur_agg: dict[str, int]
    avg_dur_agg: int


# Response models
class Film(BaseModel):
    """
    API response model for validation.

    Attriubutes:
        title (str): The title of the film.
        director (str): The director of the film.
        cast (list[str]): The cast of the film.
        country (str): The country of origin of the film.
        date_added (str): The date the film was added to Netflix.
        release_year (int): The year the film was released.
        rating (str): The rating of the film.
        duration (int): The duration of the film.
        genres (list[str]): The genres of the film.
        description (str): The description of the film.
    """
    title: str | None = ''
    director: str | None = ''
    cast: list[str] | None = []
    country: str | None = ''
    date_added: str | None = ''
    release_year: int | None = -1
    rating: str | None = ''
    duration: int | None = -1
    genres: list[str] | None = []
    description: str | None = ''

class MovieAggs(TotalAggs, DurationAggs):
    pass

class ShowAggs(TotalAggs):
    pass

class AllAggs(TotalAggs, TopAggs):
    pass


# Elasticsearch models
ELASTIC_MAP = {
    "properties": {
        "type": {"type": "byte"},
        "title": {"type": "text"},
        "director": {"type": "keyword"},
        "cast": {
            "type": "text",
            "fields": {
                "raw": {
                    "type": "keyword"}
            }
        },
        "country": {"type": "keyword"},
        "date_added": {"type": "date",
                       "format": "MMddyyyy"},
        "release_year": {"type": "integer"},
        "rating": {"type": "byte"},
        "duration": {"type": "integer"},
        "genres": {
            "type": "text",
            "fields": {
                "raw": {
                    "type": "keyword"}
                }
            },
        "description": {"type": "text"}}
}

RATING_TO_ID = {
    'PG-13': 0,
    'TV-MA': 1,
    'PG': 2,
    'TV-14': 3,
    'TV-PG': 4,
    'TV-Y': 5,
    'TV-Y7': 6,
    'R': 7,
    'TV-G': 8,
    'G': 9,
    'NC-17': 10,
    'NR': 11,
    'TV-Y7-FV': 12,
    'UR': 13
}
ID_TO_RATING = {value: key for key, value in RATING_TO_ID.items()}
