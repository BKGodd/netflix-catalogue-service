from pydantic import BaseModel


# Querying models
class Film(BaseModel):
    """
    API response model for validation.

    Attriubutes:
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

class Performer(BaseModel):
    num_movies: int
    num_shows: int
    genres: list[str]
    releases: dict[str, int]

class Actor(Performer):
    directors: list[str]

class Director(Performer):
    actors: list[str]

# Aggregation models
class TopAggs(BaseModel):
    director_agg: dict[str, int]
    actor_agg: dict[str, int]
    rating_agg: dict[str, int]
    country_agg: dict[str, int]
    genre_agg: dict[str, int]

class TotalAggs(BaseModel):
    total_agg: int

class DurationAggs(BaseModel):
    histo_dur_agg: dict[str, int]
    avg_dur_agg: int

#class PlotAgg(BaseModel):
#    movies_added_by_year: dict[int, int]
#    movies_released_by_year: dict[int, int]
#    movie_duration_hist: dict[str, int]
#    shows_added_by_year: dict[int, int]
#    shows_released_by_year: dict[int, int]


# Response models
class MovieAggs(TotalAggs, DurationAggs):
    pass

class ShowAggs(TotalAggs):
    pass

class AllAggs(TotalAggs, TopAggs):
    pass

    

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
