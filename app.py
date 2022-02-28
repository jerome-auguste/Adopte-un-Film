# %%
from flask import Flask, render_template, redirect, request, url_for
from utils import ul_fromlist, p_fromlist, tags_fromlist, score_bar, form
from sparqlRequests import get_movie, recommendation_topic
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from env import env
import json
import os
from pprint import pprint
from movie import Movie

app = Flask(__name__, static_url_path='/static')
bootstrap = Bootstrap(app)
fontawesome = FontAwesome(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.jinja_env.globals.update(ul_fromlist=ul_fromlist)
app.jinja_env.globals.update(p_fromlist=p_fromlist)
app.jinja_env.globals.update(tags_fromlist=tags_fromlist)
app.jinja_env.globals.update(score_bar=score_bar)
app.jinja_env.globals.update(form=form)
app.jinja_env.globals.update(url_for=url_for)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {}
        for i in range(0, env.num_fields_to_search):
            k = request.form.get(f'field{i}')
            v = request.form.get(f'value{i}')
            if None not in [k, v] and "" not in [k, v]:
                data[k] = v
        return redirect(f'/search/{json.dumps(data)}')
    return render_template('index.html', env=env, num_forms=[i for i in range(env.num_fields_to_search)])


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
    res = recommendation_topic(movie.uri)
    res = [Movie(dataReco=mov) for mov in res]
    return render_template('recommandations.html', main_movie=[movie], movies=res)


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
