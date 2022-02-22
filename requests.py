from SPARQLWrapper import SPARQLWrapper, JSON
import json

def get_sparql():
    return SPARQLWrapper("http://query.wikidata.org/sparql")

def get_prefix():
    return """
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX bd: <http://www.bigdata.com/rdf#>
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

def get_film(title=None, director=None, actor=None):
    query = f"""
    {get_prefix()}    
    SELECT ?film ?filmLabel ?director ?directorLabel ?actor ?actorLabel
    WHERE {{
        ?film wdt:P57 ?director ;
              wdt:P161 ?actor .
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        {search('?film', title)}
        {search('?director', director)} 
        {search('?actor', actor)} 
    }} LIMIT 100
    """
    print(query)
    sp = get_sparql()
    sp.setQuery(query)
    sp.setReturnFormat(JSON)
    results = sp.query().convert()
    print(json.dumps(results, indent=4, sort_keys=True))

print(get_film(title='inception'))
