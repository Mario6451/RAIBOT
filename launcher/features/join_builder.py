from urllib.parse import urlencode

def build_join_url(base_url, joinscript, params, values):
    query = {}

    for p in params:
        if p in values:
            query[p] = values[p]

    return f"{base_url}{joinscript}?{urlencode(query)}"
