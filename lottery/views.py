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
        'page_title':None,
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
    pass

def interview_map(request, highlight_id=None):
    pass

def public_tutorial(request):
    pass

def user_tutorial(request):
    pass


def interview_detail(request, interview_id):
    """Text Interview detail view, good for editing"""
    interview = Interview.objects.get( id=interview_id )
    template = 'lottery/interview_detail.html'
    c = {
            'page_title':None,
            'interview':interview,
            }
    return render_to_response(
            c, template )

def interview_split(request, interview_id):
    """Split map and interview"""
    interview = Interview.objects.get( id=interview_id )
    c = {
            'page_title':None,
            'interview':interview,
            }
    template = 'lottery/interview_split.html'
    return render_to_response(
            c, template )

def interview_map_detail(request, interview_id):
    """detail map view of one interview"""
    interview = Interview.objects.get( id=interview_id )
    c = {
            'page_title':None,
            'interview':interview,
            }
    template = 'lottery/interview_map_detail.html'
    return render_to_response(
            c, template )

def interview_map(request):
    """map of all interviews"""
    interviews = Interview.objects.all()
    template = 'lottery/interview_map.html'
    c = {
            'page_title':None,
            'interviews':interviews,
            }
    return render_to_response(
            c, template )

def datascope(request, area_id=None):
    """A view for accessing the datascope. area_id is either the slug of a
    borough, the slug of a neighborhood, or the number of a block group.
    The scope will zoom to the area in question.
    """
    template = 'lottery/interview_map.html'
    c = {
            'page_title':None,
            }
    pass
