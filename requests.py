from SPARQLWrapper import SPARQLWrapper, JSON

def get_sparql():
    return SPARQLWrapper("http://dbpedia.org/sparql")

def get_prefix():
    return """
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix dbo: <http://dbpedia.org/ontology/>
    prefix dbp: <http://dbpedia.org/property/>
    """

def get_film_from(director, split=True):
    if split:
        part_list = [f"'{part}'" for part in director.split()]
        director = "and".join(part_list)
    query = get_prefix() + """
    SELECT DISTINCT ?filmName ?dirName
    WHERE {
    ?film dbo:director ?director .
    ?director dbp:name ?dirName .
    ?film dbp:name ?filmName .
    ?dirName bif:contains "'nolan' and 'christopher'" .
    } LIMIT 50
    """
    sp = get_sparql()
    sp.setQuery(query)
    sp.setReturnFormat(JSON)
    results = sp.query().convert()
    return [r["filmName"]["value"] for r in results["results"]["bindings"]]

print(get_film_from("christopher nolan"))

