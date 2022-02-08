from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

# Example
# sparql.setQuery("""
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     SELECT ?label
#     WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
# """)

# Test 1
# sparql.setQuery("""
# prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# prefix db: <http://dbpedia.org/ontology/>
# SELECT DISTINCT ?film ?director 
# WHERE {
# ?film a db:Film .
# ?director a db:Person .
# ?director rdfs:director ?film .
# } LIMIT 50
# """)

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

sparql.setQuery("""
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT ?director ?director_label ?film ?film_label
WHERE {
?director wdt:P106 wd:Q2526255 .                 # has "film director" as occupation
?film wdt:P57 ?director .
SERVICE wikibase:label {
  bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".  # Get label if it exists
?director rdfs:label ?director_label .
?film rdfs:label ?film_label }
} LIMIT 100
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print(results)
for result in results["results"]["bindings"]:
    print(result["director_label"]["value"], result["film_label"]["value"])