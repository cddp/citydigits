from django.shortcuts import render_to_response, get_object_or_404

def home(request):
    """A basic home page for the citydigits project"""
    template = 'base.html'
    c = {
            'page_title':"City Digits - A Collaboration",
            }
    return render_to_response( template, c )
