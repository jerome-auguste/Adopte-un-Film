import os
from numpy import block
import requests


class Movie():
    def __init__(self, data: dict) -> None:
        self.title: str = data['filmLabel']
        self.genres = data['genresList']
        self.score = data['score']
        self.director = data['directorLabel']
        self.actors = data['actorsList']
        self.wikiurl = data['film']
        try:
            self.poster_url = data['poster']
            self.download_poster()
        except:
            pass

    def download_poster(self):
        name = self.poster_url.split('/')[-1]
        if name in os.listdir('./static'):
            self.poster_internal_url = name
            return
        with open(f'./static/{name}', 'wb') as picture:
            response = requests.get(self.poster_url, stream=True)
            if not response.ok:
                print(response)
            for memBlock in response.iter_content(1024):
                if not memBlock:
                    break
                picture.write(memBlock)
        self.poster_internal_url = name
        return
