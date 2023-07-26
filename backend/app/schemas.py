from pydantic import BaseModel


# Querying models
class Film(BaseModel):
    """
    API response model for validation.

    Attriubutes:
    """
    title: str
    director: str
    cast: list[str]
    country: str
    date_added: str
    release_year: int
    rating: str
    duration: int
    genres: list[str]
    description: str

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

    