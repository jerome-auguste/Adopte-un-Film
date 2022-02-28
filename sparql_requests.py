"""Few queries on movie search and recommandation based on wikidata endpoint"""

from SPARQLWrapper import JSON
from utils import get_sparql, get_prefix, search, resp_format # , pprint


def get_movie(title: str = None,
              director: str = None,
              actor: str = None,
              genre: str = None,
              score: int = 0) -> list:
    """Result of queries movies matching some research criteria
    (film title, director name, actor name, genre and/or minimum score)

    Args:
        title (str, optional): Searched title. Defaults to None.
        director (str, optional): Searched director. Defaults to None.
        actor (str, optional): Searched actor. Defaults to None.
        genre (str, optional): Searched genre. Defaults to None.
        score (int, optional): Minimum score. Defaults to 0.

    Returns:
        list: result of the queries
            (list of movies with id, title, director's name,
            score, poster if exists, actors list and genres list)
    """

    query = f"""
    {get_prefix()}
    SELECT ?film ?filmLabel ?directorLabel ?score
           (SAMPLE(?poster) as ?poster)
           (GROUP_CONCAT(DISTINCT ?actorLabel; separator=";") as ?actorsList)
           (GROUP_CONCAT(DISTINCT ?genreLabel; separator=";") as ?genresList)
    WHERE {{
        ?film wdt:P57 ?director ;
              wdt:P161 ?actor ;
              wdt:P136 ?genre ;
              wdt:P444 ?brutScore .
        OPTIONAL {{?film wdt:P3383 ?poster }}
        OPTIONAL {{?film wdt:P18 ?poster }}
        OPTIONAL {{?film wdt:P154 ?poster }}
        SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
            ?film rdfs:label ?filmLabel .
            ?director rdfs:label ?directorLabel .
            ?actor rdfs:label ?actorLabel .
            ?genre rdfs:label ?genreLabel .
        }}
        {search('?film', title)}
        {search('?director', director)}
        {search('?actor', actor)}
        {search('?genre', genre)}
        FILTER regex(?brutScore, "^[0-9]+%$")
        BIND(xsd:integer(REPLACE(?brutScore, "%$", "")) AS ?score)
        FILTER (?score >= {score})
    }}
    GROUP BY ?film ?filmLabel ?directorLabel ?score
    ORDER BY DESC(?score)
    LIMIT 100
    """
    # print(query)
    sp_wrapper = get_sparql()
    sp_wrapper.setQuery(query)
    sp_wrapper.setReturnFormat(JSON)
    return resp_format(sp_wrapper.query().convert()['results']['bindings'])


def recommendation_topic(film: str, limit: int=20) -> list:
    """Movie recommandations based on common main subjects with selected movie

    Args:
        film (str): URI of the selected movie
        limit (int, optional): Maximum number of results to return. Defaults to 20.

    Returns:
        list: matching moveis with URI, title,
        number of awards recieved, score on Rotten Tomato and a "relevance score"
    """

    query = f"""
    {get_prefix()}
    SELECT ?film ?filmLabel ?topicLabel (COUNT(DISTINCT ?award) AS ?numAwards) ?score ((?score + ?numAwards)*100/138 AS ?totalScore)
    WHERE {{
    {{
        SELECT ?topic
        WHERE {{ wd:{film} wdt:P921 ?topic . }}
    }}
    ?film wdt:P31 wd:Q11424 ;
          wdt:P921 ?topic ;
          wdt:P444 ?brutScore .
    OPTIONAL {{?film wdt:P166 ?award.}}
    SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" .
        ?film rdfs:label ?filmLabel .
        ?topic rdfs:label ?topicLabel .
    }}
    FILTER regex(?brutScore, "^[0-9]+%$")
    BIND(xsd:integer(REPLACE(?brutScore, "%$", "")) AS ?score)
    FILTER (?score != 100)
    FILTER(?film != wd:{film})
    }}
    GROUP BY ?film ?filmLabel ?topicLabel ?score
    ORDER BY DESC(?totalScore)
    LIMIT {limit}
    """
    # print(query)
    sp_wrapper = get_sparql()
    sp_wrapper.setQuery(query)
    sp_wrapper.setReturnFormat(JSON)
    return resp_format(sp_wrapper.query().convert()['results']['bindings'])


def recommendation_based_on(film: str, limit: int=20) -> list:
    """Movie recommandations based on same story with selected movie

    Args:
        film (str): URI of the selected movie
        limit (int, optional): Maximum number of results to return. Defaults to 20.

    Returns:
        list: matching moveis with URI, title, story on which the movie is based on,
                number of awards recieved, score on Rotten Tomato and a "relevance score"
    """

    query = f"""
    {get_prefix()}
    SELECT ?film ?filmLabel ?basedOnLabel (COUNT(DISTINCT ?award) AS ?numAwards) ?score ((?score + ?numAwards)*100/138 AS ?totalScore)
    WHERE {{
      {{ SELECT ?originBasedOn WHERE {{OPTIONAL{{wd:{film} wdt:P144 ?originBasedOn}}}}}}
      ?film wdt:P31 wd:Q11424 ;
            wdt:P136 ?genre ;
            wdt:P444 ?brutScore.
      OPTIONAL{{?film wdt:P144 ?basedOn}}
      OPTIONAL {{?film wdt:P166 ?award.}}
          
      SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" .
        ?film rdfs:label ?filmLabel .
        ?basedOn rdfs:label ?basedOnLabel.
      }}
      
      FILTER (?basedOn IN (?originBasedOn))
      FILTER regex(?brutScore, "^[0-9]+%$")
      BIND(xsd:integer(REPLACE(?brutScore, "%$", "")) AS ?score)
      FILTER (?score != 100)
      FILTER(?film != wd:{film})
    }}
    GROUP BY ?film ?filmLabel ?score ?basedOnLabel
    ORDER BY DESC(?totalScore)
    LIMIT {limit}
    """
    # print(query)
    sp_wrapper = get_sparql()
    sp_wrapper.setQuery(query)
    sp_wrapper.setReturnFormat(JSON)
    return resp_format(sp_wrapper.query().convert()['results']['bindings'])


def recommendation_part_of_series(film: str, limit: int=20) -> list:
    """Movie recommandations from the same series with selected movie

    Args:
        film (str): URI of the selected movie
        limit (int, optional): Maximum number of results to return. Defaults to 20.

    Returns:
        list: matching moveis with URI, title, series title,
                number of awards recieved, score on Rotten Tomato and a "relevance score"
    """

    query = f"""
    {get_prefix()}
    SELECT ?film ?filmLabel ?seriesLabel (COUNT(DISTINCT ?award) AS ?numAwards) ?score ((?score + ?numAwards)*100/138 AS ?totalScore)
    WHERE {{
      {{ SELECT ?series
        WHERE {{ wd:{film} wdt:P179 ?series. }}
      }}
      ?film wdt:P31 wd:Q11424 ;
            wdt:P179 ?series ;
            wdt:P444 ?brutScore.
        OPTIONAL {{?film wdt:P166 ?award.}}
          
      SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" .
        ?film rdfs:label ?filmLabel .
        ?basedOn rdfs:label ?basedOnLabel.
      }}
      FILTER regex(?brutScore, "^[0-9]+%$")
      BIND(xsd:integer(REPLACE(?brutScore, "%$", "")) AS ?score)
      FILTER (?score != 100)
      FILTER(?film != wd:{film})
    }}
    GROUP BY ?film ?filmLabel ?seriesLabel ?score
    ORDER BY DESC(?totalScore)
    LIMIT {limit}
    """
    print(query)
    sp_wrapper = get_sparql()
    sp_wrapper.setQuery(query)
    sp_wrapper.setReturnFormat(JSON)
    return resp_format(sp_wrapper.query().convert()['results']['bindings'])

def recommendation_genre(film: str, limit: int=20) -> list:
    """Movie recommandations based on common genres with selected movie

    Args:
        film (str): URI of the selected movie
        limit (int, optional): Maximum number of results to return. Defaults to 20.

    Returns:
        list: matching moveis with URI, title,
                number of awards recieved, score on Rotten Tomato and a "relevance score"
                (genre list could not be displayed because of a timeout issue with wikidata)
    """

    query = f"""
    {get_prefix()}
    SELECT ?film ?filmLabel (COUNT(DISTINCT ?award) AS ?numAwards) ?score ((?score + ?numAwards)*100/138 AS ?totalScore)
    WHERE {{
    {{
        SELECT ?originGenre
        WHERE {{ wd:{film} wdt:P136 ?originGenre . }}
    }}
    ?film wdt:P31 wd:Q11424 ;
          wdt:P136 ?genre ;
          wdt:P444 ?brutScore .
    OPTIONAL {{?film wdt:P166 ?award.}}
    SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" .
        ?film rdfs:label ?filmLabel .
        ?genre rdfs:label ?genreLabel .
    }}
    FILTER (?genre IN (?originGenre))
    FILTER regex(?brutScore, "^[0-9]+%$")
    BIND(xsd:integer(REPLACE(?brutScore, "%$", "")) AS ?score)
    FILTER (?score != 100)
    FILTER(?film != wd:{film})
    }}
    GROUP BY ?film ?filmLabel ?score
    ORDER BY DESC(?totalScore)
    LIMIT {limit}
    """
    print(query)
    sp_wrapper = get_sparql()
    sp_wrapper.setQuery(query)
    sp_wrapper.setReturnFormat(JSON)
    return resp_format(sp_wrapper.query().convert()['results']['bindings'])

def recommendation_performer(film: str, limit: int=20) -> list:
    """Movie recommandations having the same original soundtrack artist with selected movie

    Args:
        film (str): URI of the selected movie
        limit (int, optional): Maximum number of results to return. Defaults to 20.

    Returns:
        list: matching moveis with URI, title, list of performers (artists),
                number of awards recieved, score on Rotten Tomato and a "relevance score"
    """
    query = f"""
    {get_prefix()}
    SELECT ?film ?filmLabel (GROUP_CONCAT(DISTINCT ?performerLabel; separator="; ") AS ?performersList) (COUNT(DISTINCT ?award) AS ?numAwards) ?score ((?score + ?numAwards)*100/138 AS ?totalScore)
    WHERE {{
    {{
        SELECT ?originPerformer
        WHERE {{ wd:{film} wdt:P175 ?originPerformer . }}
    }}
    ?film wdt:P31 wd:Q11424 ;
          wdt:P175 ?performer ;
          wdt:P444 ?brutScore .
    OPTIONAL {{?film wdt:P166 ?award.}}
    SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" .
        ?film rdfs:label ?filmLabel .
        ?performer rdfs:label ?performerLabel .
    }}
    FILTER (?performer IN (?originPerformer))
    FILTER regex(?brutScore, "^[0-9]+%$")
    BIND(xsd:integer(REPLACE(?brutScore, "%$", "")) AS ?score)
    FILTER (?score != 100)
    FILTER(?film != wd:{film})
    }}
    GROUP BY ?film ?filmLabel ?score
    ORDER BY DESC(?totalScore)
    LIMIT {limit}
    """
    print(query)
    sp_wrapper = get_sparql()
    sp_wrapper.setQuery(query)
    sp_wrapper.setReturnFormat(JSON)
    return resp_format(sp_wrapper.query().convert()['results']['bindings'])

def recommendation_inspiredby(film: str, limit: int=20) -> list:
    """Movie recommandations from the same inspiration with selected movie

    Args:
        film (str): URI of the selected movie
        limit (int, optional): Maximum number of results to return. Defaults to 20.

    Returns:
        list: matching moveis with URI, title, inspiration list,
                number of awards recieved, score on Rotten Tomato and a "relevance score"
    """

    query = f"""
    {get_prefix()}
    SELECT ?film ?filmLabel (GROUP_CONCAT(DISTINCT ?inspiredbyLabel; separator="; ") AS ?inspiredbyList) (COUNT(DISTINCT ?award) AS ?numAwards) ?score ((?score + ?numAwards)*100/138 AS ?totalScore)
    WHERE {{
    {{
        SELECT ?originInspiredby
        WHERE {{ wd:{film} wdt:P941 ?originInspiredby . }}
    }}
    ?film wdt:P31 wd:Q11424 ;
          wdt:P941 ?inspiredby ;
          wdt:P444 ?brutScore .
    OPTIONAL {{?film wdt:P166 ?award.}}
    SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" .
        ?film rdfs:label ?filmLabel .
        ?inspiredby rdfs:label ?inspiredbyLabel .
    }}
    FILTER (?inspiredby IN (?originInspiredby))
    FILTER regex(?brutScore, "^[0-9]+%$")
    BIND(xsd:integer(REPLACE(?brutScore, "%$", "")) AS ?score)
    FILTER (?score != 100)
    FILTER(?film != wd:{film})
    }}
    GROUP BY ?film ?filmLabel ?score
    ORDER BY DESC(?totalScore)
    LIMIT {limit}
    """
    print(query)
    sp_wrapper = get_sparql()
    sp_wrapper.setQuery(query)
    sp_wrapper.setReturnFormat(JSON)
    return resp_format(sp_wrapper.query().convert()['results']['bindings'])

# res = get_film(director="Christopher Nolan")
# pprint(res)

# res = recommendation_genre('Q44578', 10)
# pprint(res)
