
class Movie():
    def __init__(self, data: dict) -> None:
        self.title = data['filmLabel']
        self.genres = data['genresList']
        self.score = data['score']
        self.director = data['directorLabel']
        self.actors = data['actorsList']
        self.wikiurl = data['film']
        try:
            self.poster_url = data['poster']
        except:
            pass
