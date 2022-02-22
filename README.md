# Movie-Selector
Design a movie request interface using the rdf based IMDB. Then try to design a simple movie recommender.

## Notes on DBs :
- IMDB does not seems to have an SPARQL endpoints.
- LinkedMDP endpoind is dead : https://www.cs.toronto.edu/~oktie/linkedmdb/sparql
- Both LinkedMDP and MovieLens would need a local dump and engine.
- Only DBpedia and Wikidata are readily usable.
    - Better text seach on DBpedia with bif:contains (FILTER(regex(...)) always time out on wikidata)
    - But more information on Wikidata (genre, rating, ...)
    - We should be able to link both with owl:sameAs.
    - Federated Quey are disabled on DBPedia, so we cannot run a conjoined search on both endpoint at the same time :(
    - Finally : mwapi allow efficient text search/filter on wikidata.
