from env import env


def ul_fromlist(list):
    return '<ul>' + '<li>'+'<li>'.join(list) + '</ul>'


def p_fromlist(list):
    return '<p>' + ', '.join(list) + '</p>'


def tags_fromlist(list):
    strr = ''
    for tag in list:
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


def score_bar(value):
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
