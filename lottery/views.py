import random # for random choice between splash pages
import os
import json
import re
import base64
import uuid
import StringIO
from pprint import pprint
from PIL import Image

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.base import ContentFile

from django.contrib.gis.geos import *

from citydigits.settings import MEDIA_ROOT
from lottery.models import (
        Interview, Question, Location, Photo, Quote, Audio,
        )

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

def data_setup(c, highlight_id=None, choose_random=False ):
    """Adds all the data to a context dictionary
        Checks input context for auth
    """

    # get everything
    questions = Question.objects.all()
    quotes = Quote.objects.all()
    audios = Audio.objects.all()
    photos = Photo.objects.all()
    interviews = Interview.objects.all()

    # setup template context
    c['questions'] = questions
    c['quotes'] = quotes
    c['audios'] = audios
    c['photos'] = photos
    c['interviews'] = interviews

    interviewGeoJsons = [n.as_geojson_feature_dict() for n in interviews]

    if interviews:
        if highlight_id:
            # find the correct interview
            interview = [i for i in interviews if str(i.id)==highlight_id][0]
            # use this point as the center
            center = interview.get_geom()
        elif choose_random:
            # random highlight for splash page
            interview = random.choice(interviews)
            center = interview.get_geom()
            highlight_id = interview.id
        else:
            # no highlighted interview
            interview = None
            # center on the centroid of all the points
            center = MultiPoint([i.get_geom() for i in interviews]).centroid

        # set highlight
        c['interview'] = interview
        c['mapcenter'] = center

    # setup javascript models context
    # all of these should use natural_key for serialization
    c['questionJsons'] = json.dumps([n.to_json_format(True) for n in questions])
    c['quoteJsons'] = json.dumps([n.to_json_format(True) for n in quotes])
    c['audioJsons'] = json.dumps([n.to_json_format(True) for n in audios])
    c['photoJsons'] = json.dumps([n.to_json_format(True) for n in photos])
    c['interviewJsons'] = json.dumps([n.to_json_format(True) for n in interviews])
    c['interviewGeoJsons'] = json.dumps(interviewGeoJsons)

    return c

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
    c.update( data_setup( c, choose_random=True) )
    templates = [
        'lottery/interview_map.html',
        'lottery/interview_photo_grid.html',
            ]
    template = random.choice( templates )
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
    c.update( data_setup( c, choose_random=True) )
    if not c['is_authenticated']:
        random.shuffle(list(c['interviews']))
    template = 'lottery/interview_photo_grid.html',
    return render_to_response( template, c )

@ensure_csrf_cookie
def interview_map(request, highlight_id=None):
    c = {
        "menu":drop_down_menu(),
        'page_title':"Interview Map - CityDigits: Lottery",
    }
    c.update( auth( request ) )
    c.update( data_setup( c, highlight_id) )
    if not c['edit_mode']:
        c.update( map_overlays() )
    template = 'lottery/interview_split.html',
    return render_to_response( template, c )

@ensure_csrf_cookie
def interview_split(request, interview_id):
    c = {
        "menu":drop_down_menu(),
        'page_title':"Interview Map Detail - CityDigits: Lottery",
    }
    c.update( auth( request ) )
    c.update( data_setup( c, interview_id) )
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

def makePhoto(data):
    dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
    imgb64 = dataUrlPattern.match(data.pop('url')).group(2)
    img_name = data['interview'] + '.jpg'
    img_file = ContentFile(imgb64.decode('base64'), name=img_name)
    image = Image.open(img_file)
    interview = Interview.objects.get(uuid=data['interview'])
    photo = Photo()
    photo.interview = interview
    photo.image = img_file
    photo.save()
    img_path = os.path.join(MEDIA_ROOT, photo.get_upload_path(img_name))
    image.save(img_path, format='JPEG')
    return {
            'remote_id':photo.id,
            'url':photo.image.url,
            }

def makeInterview(data):
    p = data['point']
    point = Point( p['lng'], p['lat'] )
    if 'remote_id' in data:
        interview = Interview.objects.get(id=data['remote_id'])
    else:
        interview = Interview()
        interview.uuid = data['uuid']
    interview.point = point
    if 'description' in data:
        interview.description = data['description']
    interview.save()
    return { 'remote_id':interview.id }

def makeAudio(data):
    pass

def makeQuote(data):
    pass

apiMakers = {
        'photo':makePhoto,
        'interview':makeInterview,
        'audio':makeAudio,
        'quote':makeQuote,
        }

def api(request, modeltype):
    """A function to handle incoming ajax data."""
    if request.method == 'POST':
        data = json.loads(request.POST['object'])
        result = apiMakers[modeltype](data)
        pprint( result )
        return HttpResponse(json.dumps(result),
                mimetype='application/javascript')

