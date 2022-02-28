from SPARQLWrapper import SPARQLWrapper, JSON
import json


def pprint(dict):
    print(print(json.dumps(dict, indent=4, sort_keys=True)))


def get_sparql():
    return SPARQLWrapper("http://query.wikidata.org/sparql")


def get_prefix():
    return """
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    """


def search(variable, target):
    if variable is None or target is None:
        return ""
    return f"""
    SERVICE wikibase:mwapi {{
      bd:serviceParam wikibase:api "EntitySearch" .
      bd:serviceParam wikibase:endpoint "www.wikidata.org" .
      bd:serviceParam mwapi:search "{target}" .
      bd:serviceParam mwapi:language "en" .
      {variable} wikibase:apiOutputItem mwapi:item .
    }}
    """


def format(res_list):
    return [
        {
            key: elm[key]['value'].split(";") if "List" in key
            else elm[key]['value']
            for key in elm
        }
        for elm in res_list
    ]


def get_film(title=None, director=None, actor=None, genre=None, score=0):
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
    print(query)
    sp = get_sparql()
    sp.setQuery(query)
    sp.setReturnFormat(JSON)
    return format(sp.query().convert()['results']['bindings'])


def recommendation_topic(film, limit=20):
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
    print(query)
    sp = get_sparql()
    sp.setQuery(query)
    sp.setReturnFormat(JSON)
    return format(sp.query().convert()['results']['bindings'])


def recommendation_based_on(film, limit=20):
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
    print(query)
    sp = get_sparql()
    sp.setQuery(query)
    sp.setReturnFormat(JSON)
    return format(sp.query().convert()['results']['bindings'])


def recommendation_part_of_series(film, limit=20):
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
    sp = get_sparql()
    sp.setQuery(query)
    sp.setReturnFormat(JSON)
    return format(sp.query().convert()['results']['bindings'])

def recommendation_genre(film, limit=20):
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
    sp = get_sparql()
    sp.setQuery(query)
    sp.setReturnFormat(JSON)
    return format(sp.query().convert()['results']['bindings'])

def recommendation_performer(film, limit=20):
    query = f"""
    {get_prefix()}
    SELECT ?film ?filmLabel (GROUP_CONCAT(DISTINCT ?performerLabel; separator="; ") AS ?performersLabel) (COUNT(DISTINCT ?award) AS ?numAwards) ?score ((?score + ?numAwards)*100/138 AS ?totalScore)
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
    sp = get_sparql()
    sp.setQuery(query)
    sp.setReturnFormat(JSON)
    return format(sp.query().convert()['results']['bindings'])

def recommendation_inspiredby(film, limit=20):
    query = f"""
    {get_prefix()}
    SELECT ?film ?filmLabel (GROUP_CONCAT(DISTINCT ?inspiredbyLabel; separator="; ") AS ?inspiredbysLabel) (COUNT(DISTINCT ?award) AS ?numAwards) ?score ((?score + ?numAwards)*100/138 AS ?totalScore)
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
    sp = get_sparql()
    sp.setQuery(query)
    sp.setReturnFormat(JSON)
    return format(sp.query().convert()['results']['bindings'])

res = get_film(director="Christopher Nolan")
pprint(res)

# res = recommendation_genre('Q44578', 10)
# pprint(res)