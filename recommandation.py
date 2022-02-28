from typing import Iterable, List
import sparql_queries
from movie import Movie
from joblib import Parallel, delayed
from env import env


class Recommandation():
    def __init__(self, uri, func, id, text) -> None:
        self.data = getattr(sparql_queries, func)(uri)
        self.data = [Movie(dataReco=mov) for mov in self.data]
        self.id = id
        self.text = text


class Recommandations():
    def __init__(self, movie) -> None:
        self.recommandations = Parallel(n_jobs=-1)(delayed(Recommandation)(movie.uri, func, func, text)
                                                   for func, text in zip(env.recommandation_functions, env.recommendation_categories))
