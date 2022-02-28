# %%
import json
import os
from flask import Flask, render_template, redirect, request, url_for
from recommandation import Recommandations
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from utils import ul_fromlist, p_fromlist, tags_fromlist, score_bar
from sparql_queries import get_movie
from env import env
import json
import os
from movie import Movie
from recommandation import Recommandations

# from pprint import pprint

app = Flask(__name__, static_url_path='/static')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap(app)
fontawesome = FontAwesome(app)
app.jinja_env.globals.update(ul_fromlist=ul_fromlist)
app.jinja_env.globals.update(p_fromlist=p_fromlist)
app.jinja_env.globals.update(tags_fromlist=tags_fromlist)
app.jinja_env.globals.update(score_bar=score_bar)
app.jinja_env.globals.update(url_for=url_for)


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {}
        for field in env.available_fields:
            value = request.form.get(f'{field}')
            if value not in [None, '']:
                data[field] = value
        return redirect(f'/search/{json.dumps(data)}')
    return render_template('index.html', env=env)


@app.route(f'/search/<data>', methods=['GET', 'POST'])
def search(data):
    data = json.loads(data)
    res = get_movie(**data)
    res = [Movie(mov) for mov in res]
    return render_template('movieList.html', movies=res)


@app.route(f'/reco/<movie>')
def recommandation(movie):
    movie = Movie(dataMovie=movie)
    if 'from_reco' in movie.__dict__ and movie.from_reco == True:
        resmov = get_movie(movie.title)
        movie = Movie(resmov[0])
    res = Recommandations(movie)
    return render_template('recommandations.html', main_movie=[movie], results=res)


@app.route('/increase')
def increase():
    env.num_fields_to_search += 1
    return redirect('/')


@app.route('/decrease')
def decrease():
    env.num_fields_to_search -= 1
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
# %%
