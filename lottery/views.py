import random # for random choice between splash pages
import json
from pprint import pprint

from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers

from lottery.models import Interview, Location

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

def public_splash(request):
    # if authenticated, go to user home
    #if request.user.is_authenticated:
        #return user_home( request )
    # this should also highlight a particular interview
    c = {
        "menu":drop_down_menu(),
        'page_title':"Home - CityDigits: Lottery",
        'splash': True,
        'interviews':Interview.objects.all(),
    }
    templates = [
        'lottery/interview_map.html',
        'lottery/interview_photo_grid.html',
            ]
    template = random.choice( templates )
    return render_to_response( template, c )

def user_home(request):
    pass

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
    template = 'lottery/interview_photo_grid.html',
    return render_to_response( template, c )

def interview_map(request, highlight_id=None):
    # get the interviews
    interview_fields = (
            'id',
            'body',
            'location_id',
            )
    interviews = Interview.objects.all()
    locations = [n.as_geojson_feature( interview_fields ) for n in interviews]
    c = {
        "menu":drop_down_menu(),
        'page_title':"Interview Map - CityDigits: Lottery",
        'interviews':json.dumps(locations, indent=2),
    }
    template = 'lottery/interview_map.html',
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


def interview_detail(request, interview_id):
    interview = Interview.objects.get(id=interview_id)
    c = {
        "menu":drop_down_menu(),
        'page_title':"Interview %s - CityDigits: Lottery: Lottery" % interview_id,
        'interview':interview,
    }
    template = 'lottery/interview_detail.html',
    return render_to_response( template, c )

def interview_split(request, interview_id):
    pass

def interview_map_detail(request, interview_id):
    pass
