from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON
import json

def set_language_filters(language):
    if language == 'default':
        return ['', '']
    filter_lang_label = "filter(lang(?label) = \'" + language + "\')\n"
    filter_lang_comment = "filter(lang(?comment) = \'" + language + "\')\n"
    return [filter_lang_label, filter_lang_comment]

def send_query(top, bottom, left, right, language):
    sparql = SPARQLWrapper('http://dbpedia.org/sparql')

    # Prepare filters
    filter_latitude = "?lat > " + str(bottom) + " && ?lat < " + str(top)
    filter_longitude = "?long > " + str(left) + " && ?long < " + str(right)

    filter_lang_label, filter_lang_comment = set_language_filters(language)

    sparql.setQuery("""
        PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX yago: <http://dbpedia.org/class/yago/>

        SELECT DISTINCT
        ?name ?lat ?long (MIN(?label) AS ?label) (MIN(?comment) AS ?comment)
        WHERE {
            ?name rdf:type yago:Company108058098.
            ?name geo:lat ?lat.
            ?name geo:long ?long.

            filter(""" + filter_latitude + """ && """ + filter_longitude + """)
            OPTIONAL {
            ?name rdfs:label ?label.
            ?name rdfs:comment ?comment.

            """ + filter_lang_label + filter_lang_comment + """
            }
        }
        GROUP BY ?name ?lat ?long
        LIMIT 20
    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results

def get_value_of_key(dictionary, key, value):
    if dictionary.get(key, False):
        return unicode(dictionary[key][value])
    return 'No value found in dbpedia'

def json_to_dictionary(results):
    list_of_results = []
    for result in results['results']['bindings']:
        list_of_results.append(
            {
                'name' : unicode(result['name']['value']),
                'label' : get_value_of_key(result, 'label', 'value'),
                'comment' : get_value_of_key(result, 'comment', 'value'),
                'latitude' : result['lat']['value'],
                'longitude' : result['long']['value'],
            }
        )
    return list_of_results

def get_companies(latitude, longitude, tolerance, language):
    # Prepare boundaries
    top = latitude + tolerance
    bottom = latitude - tolerance
    left = longitude - tolerance
    right = longitude + tolerance

    results = send_query(top, bottom, left, right, language)

    # Conver json from dbpedia to json that is suitable for d3.js
    return json.dumps(json_to_dictionary(results))
