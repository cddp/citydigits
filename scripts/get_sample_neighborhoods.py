import os
import json
from pprint import pprint, pformat

from geese.db import GeeseDB

dbinfo = {
        'NAME':'lottery',
        'USER':'bengolder',
        'PASSWORD':'D44A?+aM',
        }
fields = [
 'boro',
 'borough',
 'med_income',
 'name',
 'nyc_neig',
 'pop',
        ]
localpath = 'lottery/sample_data/neighborhoods.py'
jspath = 'citydigits/static/js/neighborhoods.js'

def get_neighborhoods():
    db = GeeseDB(dbinfo)
    nhoods = db.layer('neighborhoods')
    qset = nhoods.objects.all()
    with open(jspath, 'w') as f:
        f.write('var neighborhoods = [\n')
        for n in qset:
            d = n.as_geojson_feature_dict(fields,4326)
            f.write(json.dumps(d))
            f.write(',\n')
        f.write('];\n')

def get_boroughs():
    db = GeeseDB(dbinfo)
    boroughs = db.layer('boroughs').objects.all()
    borough_data = [n.as_geojson_feature_dict(['boroname'],4326) for n in boroughs]
    with open(localpath, 'w') as f:
        f.write(pformat(borough_data))




get_boroughs()
