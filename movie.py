import os
from numpy import block
import requests
import json


class Movie():
    def __init__(self, dataSparql: dict = None, dataMovie: dict = None, dataReco: dict = None) -> None:
        if dataSparql is not None:
            self.init_from_search(dataSparql)
        elif dataMovie is not None:
            self.load(dataMovie)
        elif dataReco is not None:
            self.init_from_reco(dataReco)

    def init_from_search(self, data):
        self.title: str = data['filmLabel']
        self.genres: list = data['genresList']
        self.score: str = data['score']
        self.director: str = data['directorLabel']
        self.actors: list = data['actorsList']
        self.wikiurl: str = data['film']
        self.uri: str = data['film'].split('/')[-1]
        try:
            self.poster_url = data['poster']
            self.download_poster()
        except:
            pass

    def load(self, data):
        data = json.loads(data)
        for k, v in data.items():
            self.__setattr__(k, v)
        self.unscramble_url()

    def init_from_reco(self, data):
        self.wikiurl: str = data['film']
        self.title: str = data['filmLabel']
        self.topic: str = data['topicLabel']
        self.score: str = data['score']
        self.uri: str = data['film'].split('/')[-1]
        self.from_reco = True

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

    def scramble_url(self):
        for k, v in self.__dict__.items():
            if type(v) is str:
                self.__setattr__(k, v.replace('/', '|'))

    def unscramble_url(self):
        for k, v in self.__dict__.items():
            if type(v) is str:
                self.__setattr__(k, v.replace('|', '/'))

    def to_json(self):
        self.scramble_url()
        return json.dumps({k: v for k, v in self.__dict__.items()})
