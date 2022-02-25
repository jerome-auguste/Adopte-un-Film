# %%
from flask import Flask, render_template, redirect, request
from utils import ul_fromlist
from requests import get_film
from flask_bootstrap import Bootstrap
from env import env
import json
import os
from pprint import pprint
from movie import Movie

app = Flask(__name__)
bootstrap = Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {}
        for i in range(0, env.num_fields_to_search):
            k = request.form.get(f'field{i}')
            v = request.form.get(f'value{i}')
            if None not in [k, v] and "" not in [k, v]:
                data[k] = v
        return redirect(f'/search={json.dumps(data)}')
    return render_template('index.html', env=env)


@app.route(f'/search=<data>')
def search_2(data):
    print(data)
    data = json.loads(data)
    res = get_film(**data)
    pprint(res)
    res = [Movie(mov) for mov in res]
    return render_template('movieList.html', movies=res)


if __name__ == '__main__':
    app.run(debug=True)
# %%
