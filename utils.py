"""Utility functions used for the project"""
import json
from SPARQLWrapper import SPARQLWrapper
from env import env

# ----------------------------- Utilities for backend and frontend -----------------------------
def ul_fromlist(python_list: list) -> str:
    """Formatting list for HTML

    Args:
        python_list (list): python list to format for HTML

    Returns:
        str: HMTL code for the list
    """
    return '<ul>' + '<li>'+'<li>'.join(python_list) + '</ul>'


def p_fromlist(python_list: list) -> str:
    """Formatting list into paragraph in HTML

    Args:
        python_list (list): python list to format

    Returns:
        str: HMTL code for the list
    """
    return '<p>' + ', '.join(python_list) + '</p>'


def tags_fromlist(python_list: list) -> str:
    """Format python list into a set of tags in HTML

    Args:
        python_list (list): python list to format

    Returns:
        str: Tag formatted list in HTML
    """
    strr = ''
    for tag in python_list:
        strr += f"<button type='button' class='btn btn-outline-info mr-2 mb-1'>{tag}</button>"
    return strr


def form(num):
    options = ''.join(
        [f"<option value='{opt}'> {opt} </option>" for opt in env.available_fields])

    return f"""<div class="form-group m-2">
                    <div class='col'>
                        <div class= 'row'>
                                <label for="field{num}">Field</label>
                                <select class='form-control' name="field{num}">""" +\
        """<option value="{{None}}" selected></option>""" + options +\
        """</select>
                        </div>
                        <div class= 'row'> """ +\
        f"""<label for="value{num}">Value</label>
                            <input type="text" class='form-control' name="value{num}" placeholder="">
                        </div>
                    </div>
                </div>"""


def score_bar(value: float) -> str:
    """Score bar in HTML

    Args:
        value (float): Value of the score (between 0 and 100)

    Returns:
        str: HTML code for the score bar
    """

    return f"""<div class='progress'>
                    <div    class='progress-bar progress-bar-striped progress-bar-animated'
                            role='progressbar'
                            aria-valuenow='{value}'
                            aria-valuemin='0'
                            aria-valuemax='100'
                            style='width: {value}%'>
                    {value}%
                    </div>
                </div>"""

# ----------------------------- Utilities for sparql queries -----------------------------

def pprint(python_dict: dict) -> None:
    """Pretty printer for json objects, only for dev purposes

    Args:
        dict (dict): input dictionnary in json format
    """

    print(print(json.dumps(python_dict, indent=4, sort_keys=True)))


def get_sparql() -> SPARQLWrapper:
    """Utility function for SPARQL endpoint

    Returns:
        SPARQLWrapper: instance of a wrapper to make queries
    """

    return SPARQLWrapper("http://query.wikidata.org/sparql")


def get_prefix() -> str:
    """Beginning of all queries (prefixes used in the different queries in the project)

    Returns:
        str: Prefix lines
    """

    return """
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    """


def search(variable: str, target: str) -> str:
    """Search serice using mwapi on wikidata

    Args:
        variable (str): variable name (?film, ?director...)
        target (str): value to search for

    Returns:
        str: service query
    """

    if variable is None or target is None:
        return ""
    return f"""
    SERVICE wikibase:mwapi {{
      bd:serviceParam wikibase:api "EntitySearch" .
      bd:serviceParam wikibase:endpoint "www.wikidata.org" .
      bd:serviceParam mwapi:search "{target}" .
      bd:serviceParam mwapi:language "en" .
      {variable} wikibase:apiOutputItem mwapi:item .
    }}
    """


def resp_format(res_list: list) -> list[dict]:
    """Format query result into a dictionnary

    Args:
        res_list (list): list of elements in the query response

    Returns:
        list: formatted response (list[dict])
    """

    return [
        {
            key: elm[key]['value'].split(";") if "List" in key
            else elm[key]['value']
            for key in elm
        }
        for elm in res_list
    ]
