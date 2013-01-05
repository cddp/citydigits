import random # for random choice between splash pages

from django.shortcuts import render_to_response, get_object_or_404
from lottery.models import Interview

# drop down menu contents
def drop_down_menu():
    # just return a dictionary of stuff
    d = {
        'small':{
            'contents':"",
            "links":[
                {
                    'url':"/lottery/login/",
                    'text':"BSSJ Student Login",
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
                    'url':"/lottery", # this url does nothing at the moment
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
    c = {
        "menu":drop_down_menu(),
        'page_title':"Home - CityDigits",
        #'interviews':interviews,
        'splash':True,
        'scripts':[
            'jquery.min.js',
            'drop_down_menu.js',
            ],
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
    pass

def interview_photo_grid(request):
    c = {
        "menu":drop_down_menu(),
        'page_title':"Interviews - CityDigits",
        #'interviews':interviews,
        'splash':False,
        'scripts':[
            'jquery.min.js',
            'drop_down_menu.js',
            ],
    }
    template = 'lottery/interview_photo_grid.html',
    return render_to_response( template, c )

def interview_map(request, highlight_id=None):
    c = {
        "menu":drop_down_menu(),
        'page_title':"Interview Map - CityDigits",
        #'interviews':interviews,
        'splash':False,
        'scripts':[
            'jquery.min.js',
            'drop_down_menu.js',
            ],
    }
    template = 'lottery/interview_map.html',
    return render_to_response( template, c )

def public_tutorial(request):
    pass

def user_tutorial(request):
    pass


def interview_detail(request, interview_id):
    pass

def interview_split(request, interview_id):
    pass

def interview_map_detail(request, interview_id):
    pass
