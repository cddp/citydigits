import random # for random choice between splash pages
import json
from pprint import pprint

from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers

from django.contrib.gis.geos import *

from lottery.models import Interview, Location, Photo

from django.forms.models import model_to_dict
from lottery.sample_data import sample_data as sample
from lottery.sample_data import sample_interview

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

def user_menu():
    d = {
            }
    return d

def auth(request):
    # randomly select auth and edit settings
    isAuth = bool(random.randint(0,1))
    isEdit = bool(random.randint(0,1))
    return {
            'is_authenticated':isAuth,
            'edit_mode':isEdit,
            }

def pick_a_few(things):
    selected = []
    amounts = [1, 1, 0, random.randint(0,3)]
    amount = random.choice(amounts)
    for i in range(amount):
        selected.append( random.choice(things) )
    return selected

def is_complete_interview(interview):
    if not interview.photos:
        return False

def interview_test_data():
    d = {}
    interviews = Interview.objects.all()
    interview_dicts = [i.to_dict( exclude=['body']) for i in interviews]
    locations = []
    for i in interviews:
        location = i.location.to_dict()
        locations.append(location)
    photos = Photo.objects.all()
    photos = [p.to_dict(True, exclude=['date_added']) for p in photos]
    descriptions = sample.descriptions
    audios = sample.audios
    questions = sample.questions
    quotes = sample.quotes
    # make sure we have interview jsons
    # tie the photos together
    for i in interview_dicts:
        i['description'] = random.choice([random.choice(descriptions), ""])
        i['photos'] = pick_a_few(photos)
        i['questions'] = []
        for n, q in enumerate(questions):
            question = {'id':n,'text':q,'audios':[]}
            these_mp3s = pick_a_few(audios)
            for a in these_mp3s:
                obj = {}
                obj['url'] = a
                obj['quotes'] = pick_a_few(quotes)
                question['audios'].append(obj)
            i['questions'].append(question)
    d['interviews'] = interview_dicts
    d['interviewJsons'] = json.dumps(interview_dicts)
    d['questionJsons'] = json.dumps(questions)
    return d

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


def map_context(highlight_id=None, choose_random=False):
    # get the interviews
    interview_fields = (
            'id',
            'location_id',
            )
    interviews = Interview.objects.all()
    photos = [i.photo_set.all()[0] for i in interviews]
    # layers (fake for now)
    layers = {
            "Interviews":"OFF",
            "Lottery Sales":"ON",
            "Population":"OFF",
            "Commercial Areas":"ON",
            }
    if highlight_id:
        # find the correct interview
        interview = [i for i in interviews if str(i.id)==highlight_id][0]
        # use this point as the center
        center = interview.location.geom()
    elif choose_random:
        # random highlight for splash page
        interview = random.choice(interviews)
        center = interview.location.geom()
        highlight_id = interview.id
    else:
        # no highlighted interview
        interview = None
        # center on the centroid of all the points
        center = MultiPoint([i.location.geom() for i in interviews]).centroid
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
        'maplayers': layers,
        }

def interview_map(request, highlight_id=None):
    c = {
        "menu":drop_down_menu(),
        'page_title':"Interview Map - CityDigits: Lottery",
    }
    c.update( interview_test_data() )
    c.update( map_context( highlight_id ) )
    c.update( auth( request ) )
    template = 'lottery/interview_map.html',
    return render_to_response( template, c )

def interview_split(request, interview_id):
    c = {
        "menu":drop_down_menu(),
        'page_title':"Interview Map Detail - CityDigits: Lottery",
    }
    c.update( map_context( interview_id ) )
    c.update( interview_test_data() )
    c.update( interview_detail_context( c ) )
    c.update( auth( request ) )
    template = 'lottery/interview_split.html',
    return render_to_response( template, c )

def interview_detail(request, interview_id):
    interview = sample_interview
    c = {
        "menu":drop_down_menu(),
        'page_title':"Interview %s - CityDigits: Lottery: Lottery" % interview_id,
    }
    c.update( interview_detail_context( interview_id ) )
    template = 'lottery/interview_detail.html',
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

def interview_map_detail(request, interview_id):
    pass
