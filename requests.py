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

def get_film(title=None, director=None, actor=None, genre=None):
    query = f"""
    {get_prefix()}    
    SELECT ?filmLabel ?directorLabel 
           (GROUP_CONCAT(DISTINCT ?actorLabel; separator=", ") as ?actorsLabel)
           (GROUP_CONCAT(DISTINCT ?genreLabel; separator=", ") as ?genresLabel)
    WHERE {{
        ?film wdt:P57 ?director ;
              wdt:P161 ?actor ;
              wdt:P136 ?genre .
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
    }}
    GROUP BY ?filmLabel ?directorLabel
    LIMIT 100
    """
    print(query)
    sp = get_sparql()
    sp.setQuery(query)
    sp.setReturnFormat(JSON)
    return sp.query().convert()['results']['bindings']

res = get_film(director='nolan')
pprint(res)
