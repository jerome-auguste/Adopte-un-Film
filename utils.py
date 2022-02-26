
def ul_fromlist(list):
    return '<ul>' + '<li>'+'<li>'.join(list) + '</ul>'


def p_fromlist(list):
    return '<p>' + ', '.join(list) + '</p>'


def tags_fromlist(list):
    strr = ''
    for tag in list:
        strr += f"<button type='button' class='btn btn-outline-info mr-2'>{tag}</button>"
    return strr


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
