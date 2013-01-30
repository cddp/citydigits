from geese.db import GeeseDB
import json
from lottery.sample_data.neighborhoods import boroughs

localpath = 'lottery/sample_data/neighborhoods.geojson'


layers = [
        {
        "full_name": "Total Lottery Sales",
        "name":"sales",
        "type":"mapbox_hover",
        "mapbox_url":"sw2279.NewYorkSales",
        "status": "ON",
        },
        {
        "full_name": "Boroughs",
        "name": "boroughs",
        "type": "geoJson",
        "status": "ON",
        "features":boroughs,
        },
]
