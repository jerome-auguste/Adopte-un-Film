# Movie-Selector
Design a movie request interface using the rdf based IMDB. Then try to design a simple movie recommender.

## Setup :
1. Clone the repo
2. Install the requirements with `pip install -r requirements.txt` at the root of the repo
3. Optionnal but necessary sometimes: run `export FLASK_APP=app`
4. Run the command `flask run` at the root of the repo

## How to use :
- Select a field and provide a value for it, repeat for any number of filter, then click the "search" button.
- On the search results page, you can consult the wikidata page of each movie, or ask for similar movies for each movie.
- On the recommendation page, you can consult the wikidata page of each movie, or click on the "similar movies" button on a card to have more informations about a movie.

## Notes on ontologies :
Text based selection is mandatory to be able to recommend film by director, actor or genre, since we cannot expect users to know the properties ID.
Thus, the choice of the ontology depended on *endpoint availability* and the ability to make *efficient text based selection*, as the usual `(FILTER(regex(...))` timeout more often than not. 
- IMDB does not seems to have a SPARQL endpoint.
- LinkedMDP's endpoind is dead : https://www.cs.toronto.edu/~oktie/linkedmdb/sparql
- Both LinkedMDP and MovieLens would need a local dump and engine, as well as be severely outdated.
- Only DBpedia and Wikidata are readily usable.
    - Efficient text filter on DBpedia with `bif:contains`. `(FILTER(regex(...))` always time out on wikidata, and `bif:contains` is not available there.
    - However, DBPedia has far fewer information than Wikidata. Properties such as `genre` and `rating` are missing.
    - We should be able to link both ontology with `owl:sameAs`, but federated query are disabled on DBPedia, so we cannot run a conjoined search on both endpoint at the same time...
    - Finally, `mwapi` allow efficient text search on wikidata. *Warning* : it is NOT a text filter like `regex` or `bif:contains`, but more of an indexed search like Google (that's probably why it doesn't time out). It may not match anything for a standard word like 'the', or a name like 'scott', but will find matches for more specific strings like 'ridley scott' or 'nolan'.
