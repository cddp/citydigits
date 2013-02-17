import random # for random choice between splash pages
import json
import re
import base64
import uuid
import cStringIO
from pprint import pprint
from PIL import Image

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie

from django.contrib.gis.geos import *

from lottery.models import Interview, Location, Photo

from django.forms.models import model_to_dict
from lottery.sample_data import sample_data as sample
from lottery.sample_data import sample_interview
from lottery.sample_data import sample_layers

# drop down menu contents
def drop_down_menu():
    # just return a dictionary of stuff
    d = {
        'small':{
            'contents':"",
            "links":[
                {
                    'url':"/login/",
                    'text':"User Login",
                },
                {
                    'url':"/lottery/interviews/",
                    'text':"Browse Interviews",
                },
                {
                    'url':"/lottery/map/",
                    'text':"Explore the Map",
                },
                {
                    'url':"/lottery/data/", # this url does nothing at the moment
                    'text':"Explore the Data",
                },
                ]
            }
    }
    return d

def auth(request):
    # randomly select auth and edit settings
    isAuth = bool(random.randint(0,1))
    if isAuth:
        isEdit = bool(random.randint(0,1))
    else:
        isEdit = False
    return {
            'is_authenticated':True,
            'edit_mode':True,
            }

@ensure_csrf_cookie
def public_splash(request):
    # if authenticated, go to user home
    # if request.user.is_authenticated:
        #return user_home( request )
    # this should also highlight a particular interview
    c = {
        "menu":drop_down_menu(),
        'page_title':"Home - CityDigits: Lottery",
        'splash': True,
    }
    c.update( auth( request ) )
    templates = [
        'lottery/interview_map.html',
        'lottery/interview_photo_grid.html',
            ]
    template = random.choice( templates )
    if 'map' not in template:
        c['interviews'] = list(Interview.objects.all())
        random.shuffle(c['interviews'])
    else:
        c.update( map_context(choose_random=True) )
    return render_to_response( template, c )

def about(request):
    c = {
        "menu":drop_down_menu(),
        'page_title':"About - CityDigits: Lottery",
        #'interviews':interviews,
    }
    template = "lottery/about.html"
    return render_to_response( template, c )

@ensure_csrf_cookie
def interview_photo_grid(request):
    c = {
        "menu":drop_down_menu(),
        'page_title':"Interviews - CityDigits: Lottery",
        'interviews':Interview.objects.all(),
    }
    c.update( auth( request ) )
    random.shuffle(list(c['interviews']))
    template = 'lottery/interview_photo_grid.html',
    return render_to_response( template, c )

def interview_detail_context(c):
    return {
            'interview':random.choice(c['interviews'])
                }

def map_overlays():
    # get sample layers
    mapbox_layers = []
    geojson_layers = []
    layers = []
    for layer in sample_layers.layers:
        if 'mapbox' in layer['type']:
            mapbox_layers.append(layer)
        elif layer['type'] == 'geoJson':
            geojson_layers.append( layer )
        layers.append( layer )
    return {
        'maplayers': layers,
        'maplayerJsons': json.dumps(layers),
        'mapbox_layers':mapbox_layers,
        'geojson_layers':json.dumps(geojson_layers),
        }

def map_context(highlight_id=None, choose_random=False):
    # get the interviews
    interview_fields = (
            'id',
            'location_id',
            )
    interviews = Interview.objects.all()
    photos = [i.photo_set.all()[0] for i in interviews]
    if highlight_id:
        # find the correct interview
        interview = [i for i in interviews if str(i.id)==highlight_id][0]
        # use this point as the center
        center = interview.location.get_geom()
    elif choose_random:
        # random highlight for splash page
        interview = random.choice(interviews)
        center = interview.location.get_geom()
        highlight_id = interview.id
    else:
        # no highlighted interview
        interview = None
        # center on the centroid of all the points
        center = MultiPoint([i.location.get_geom() for i in interviews]).centroid
    # turn the interviews into geojson features
    locations = [n.as_geojson_feature( interview_fields ) for n in interviews]
    # add the photos
    for i, loc in enumerate(locations):
        loc['properties']['photo'] = photos[i].image.url
    # return a context dictionary
    return {
        'selected_interview': highlight_id,
        'interviewGeoJsons':json.dumps(locations),
        'mapcenter':center.coords,
        'interview':interview,
        }

@ensure_csrf_cookie
def interview_map(request, highlight_id=None):
    c = {
        "menu":drop_down_menu(),
        'page_title':"Interview Map - CityDigits: Lottery",
    }
    c.update( interview_test_data() )
    c.update( map_context( highlight_id ) )
    c.update( auth( request ) )
    if not c['edit_mode']:
        c.update( map_overlays() )
    template = 'lottery/interview_map.html',
    return render_to_response( template, c )

@ensure_csrf_cookie
def interview_split(request, interview_id):
    c = {
        "menu":drop_down_menu(),
        'page_title':"Interview Map Detail - CityDigits: Lottery",
    }
    c.update( map_context( interview_id ) )
    c.update( interview_detail_context( c ) )
    c.update( auth( request ) )
    template = 'lottery/interview_split.html',
    return render_to_response( template, c )

def edit_map(request):
    c = {
        "menu":drop_down_menu(),
        'page_title':"Interview Map - CityDigits: Lottery",
        'interviews':Interview.objects.all(),
    }
    template = 'lottery/interview_map_edit.html',
    return render_to_response( template, c )

def data_explorer(request):
    c = {
        "menu":drop_down_menu(),
        'page_title':"Data Explorer - CityDigits: Lottery: Lottery",
        #'interviews':interviews,
    }
    template = 'lottery/data_explorer.html',
    return render_to_response( template, c )

def public_tutorial(request):
    pass

def user_tutorial(request):
    pass

def handleImageData(photoObj):
    dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
    imgb64 = dataUrlPattern.match(photoObj['url']).group(2)
    if imgb64 is not None and len(imgb64) > 0:
        tempImg = cStringIO.StringIO(imgb64.decode('base64'))
        image = Image.open(tempImg)
        print image
    return image

def api(request, modeltype):
    """A function to handle incoming ajax data."""
    if request.method == 'POST':
        print request.user{{
        data = request.POST
        if modeltype == 'photo':
            handleImageData(data)
        else:
            print dict(data)
        d = {}
        d['success'] = True
        d['something_else'] = 'hello'
        return HttpResponse(json.dumps(d),
                mimetype='application/javascript')

