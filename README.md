# :tv: Adopte un Film :tv:

## :computer: Contributors

- [Jérôme AUGUSTE](https://github.com/jerome-auguste)
- [Nathan BRUCKMANN](https://github.com/kim0n0)
- [Ruben PARTOUCHE](https://github.com/rbpart)

## :page_facing_up: Context and introduction

In the context of the Reasionning and Knowledge Representation course, we designed a movie request interface using the rdf based database ([Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page)) and made a custom recommender from a selected movie.
The database is used for more general purposes but we only focused on movies for our project.

## :file_folder: Architecture of the code

```text
.
├── app.py                      # Back end script
├── env.py                      # Environment variables
├── movie.py                    # Handling movie data with a class
├── recommandation.py           # Recommendation class (to integrate multiple recommendation functions)
├── sparql_queries.py           # All the parametrized SPARQL queries of the project
├── utils.py                    # Utilities for queries (prefix, formatting...) and back end
├── static                      # Static media
│   └── font-awesome            # Font awesome style files
│
├── templates                   # HTML templates to display results
│   ├── index.html              # Home page
│   ├── movieList.html          # Search engine
│   └── recommandations.html    # Recommendation engine
│
├── requirements.txt    
├── LICENSE
├── .gitignore
└── README.md

```

## :runner: Run the code

1. Clone the repo in the destination folder of your choice (or unzip the archive)
2. Navigate to the root of this repo in your terminal
3. Run the command `pip install -r requirements.txt` to install dependencies (either on a venv or a general Python distribution)
4. Run the command `flask run` to run the server
5. Open the generated link in your web browser (usually `http://127.0.0.1:5000/`)

## :mag: Guidelines of our solution

After opening the aforementioned link in your browser, few intuitive steps are described here to take full advantage of the service:

- Fill in one or more fields to look for a movie, then click on search or press `enter` (it might take some time because of wikidata's bottleneck)
- On the results page, each movie has its own Wikidata button to consult full details in the database or a *recommendation* button to find similar movies.
- After clicking on `More movies like this`, recommended movies are categorised depending on the type of similarity it has with the selected movie. you can consult their associated Wikidata page, or click on the `More info` button on a card to have more information about a movie and other recommended movies.

## :bulb: Main ideas

Used queries are printed in real time in the terminal where flask was launched (for dev purposes).

### Search engine

The movie search engine is quite simple and relies on the most comon attributes (title, director, a main actor, genre and/or minimum review score on Rotten Tomato) as filters. The query is parametrised so the user can fill as much fields as he wants to. A ranking of the results is made thanks to the review score.

### Recommendation engine

The recommendations can be based on several criteria from the selected movies. Few of them were selected as the most relevant ones:

- Similar subjects (e.g. gambling, terrorism...)
- Same story (e.g. Batman...)
- Other movies of a series (Batman series, James Bond series...)
- In the same genre (e.g. thriller)
- With the same Original Soundtrack performer (e.g. Hans Zimmer)
- From similar inspirations (field: `inspired by`)

Moreover, a *Relevance scoring* has been made using both number of awards recieved and the review score, in order to rank the recommended movies.

## :warning: Notes on ontologies

Text based selection is mandatory to be able to recommend film by director, actor or genre, since we cannot expect users to know the properties ID.
Thus, the choice of the ontology depended on *endpoint availability* and the ability to make *efficient text based selection*, as the usual `(FILTER(regex(...))` timeout more often than not.

- IMDB does not seems to have a SPARQL endpoint.
- [LinkedMDP's endpoint](https://www.cs.toronto.edu/~oktie/linkedmdb/sparql) is dead
- Both LinkedMDP and MovieLens would need a local dump and engine, as well as be severely outdated.
- Only DBpedia and Wikidata are readily usable.
  - Efficient text filter on DBpedia with `bif:contains`. `(FILTER(regex(...))` always time out on wikidata, and `bif:contains` is not available there.
  - However, DBPedia has far fewer information than Wikidata. Properties such as `genre` and `rating` are missing.
  - We should be able to link both ontology with `owl:sameAs`, but federated query are disabled on DBPedia, so we cannot run a joined search on both endpoint at the same time...
- Finally, `mwapi` allows efficient text search on wikidata. *Warning* : it is NOT a text filter like `regex` or `bif:contains`, but more of an indexed search like Google (that's probably why it doesn't time out). It may not match anything for a standard word like 'the', or a name like 'scott', but will find matches for more specific strings like 'ridley scott' or 'nolan'.

## :warning: Notes on search and recommendation engines

We decided to focus on Rotten Tomato score to have an out of 100 number that could rank the movies

Limitting the number of instances helps in keeping the webpage light.

### Search engine notes

*Posters* can be downloaded when available, and can fallback to an image, or even to a logo, if it is missing. However, most movies do not have any sort of associated image on wikidata. Therefore, no picture has been added to the solution (even though they still are included in the queries for academic purposes)

### Recommendation engine notes

- Time out issues forces to keep complexity at a low level. Complex similitude criterion, such as movies with the most number of common genre and actor, will time out.
- Genres could not be loaded in the *Similar genres* recommendation part as trying to list all genres of each movie made the endpoint timeout
- Sores of 100 were filtered out to reduce noise generated by unpopular movies that got rated at the maximum grade by one reviewer only.

## :hourglass_flowing_sand: Further improvements

In order to give more information about a movie, one can try to combine more movie databases and aggregate some data

Other improvement could be investigated in optimising the queries to prevent timeout on complex aggregation functions either to give more information or to improve the *Relevance score* (using similarity functions such as the number of actors in common...)
