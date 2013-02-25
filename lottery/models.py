from django.contrib.gis.db import models
from django.contrib.auth.models import User

from citydigits.settings import MEDIA_ROOT
from geese.models import GeeseModel
from datertots.models import  DataModel, UUIDModel
from datertots.models import model_to_dict

def get_upload_path(instance, filepath):
    return instance.get_upload_path(filepath)

class UserProfile( DataModel, UUIDModel ):
    """This class should store information about a user who uploads interviews.
    """
    user = models.OneToOneField( User )
    name = models.CharField( max_length=500 )
    def __unicode__(self):
        return self.name

class LocationManager(models.GeoManager):
    def get_by_natural_key(self, point):
        self.get( point=point )

class Location( GeeseModel ):
    """For storing the locations, of retailers or interviews."""
    point = models.PointField( null=True, blank=True )
    address_text = models.TextField( null=True, blank=True )
    street_address = models.CharField( max_length=500, null=True, blank=True )
    raw_address_text = models.TextField( null=True, blank=True )
    city = models.CharField( max_length=100, null=True, blank=True )
    state = models.CharField( max_length=100, null=True, blank=True )
    zipcode = models.CharField( max_length=100, null=True, blank=True )

    objects = LocationManager()

    def __unicode__(self):
        if self.point:
            return 'Location: %s' % str(self.point.coords)
        else:
            return self.address_text

    def natural_key(self):
        return self.point

class RetailerManager(models.Manager):
    def get_by_natural_key(self, retailer_id):
        self.get( retailer_id=retailer_id )

class Retailer( DataModel ):
    """For storing distinct retailer names and retailer IDs
    """
    name = models.CharField( max_length = 500 )
    retailer_id = models.CharField( max_length = 100 )
    location = models.ForeignKey( Location, null=True, blank=True )
    objects = RetailerManager()
    def __unicode__(self):
        return '%s: %s' % ( self.retailer_id, self.name )
    def natrual_key(self):
        return self.retailer_id

class SalesWeek( DataModel ):
    """For storing one week of sales at a particular place.
    """
    week = models.DateField()
    amount = models.FloatField()
    retailer = models.ForeignKey( Retailer )

    def __unicode__(self):
        return '%s, %s: $%s' % ( self.retailer.name, self.week, self.amount )

class Win( DataModel ):
    """For storing a winning ticket.
    """
    date = models.DateField()
    retailer = models.ForeignKey( Retailer )
    amount = models.FloatField()
    game = models.CharField( max_length=300 )
    def __unicode__(self):
        return '%s $%s at %s on %s' % ( self.game, self.amount,
                self.retailer.name, self.date)




class Interview( GeeseModel, UUIDModel ):
    """A class for storing information about interviews."""
    point = models.PointField()
    description = models.CharField( max_length=300, null=True, blank=True )
    date_added = models.DateTimeField( auto_now_add=True )
    date_edited = models.DateTimeField( auto_now=True )
    creators = models.ManyToManyField( 'UserProfile', null=True, blank=True )

    def __unicode__(self):
        if self.description:
            return self.description
        else:
            return self.point.wkt

    def is_complete(self):
        """This method checks if the interview has sufficient information to be
        displayed to the public.
        """
        # is there a description?
        if not self.description:
            return False
        # was it made by someone?
        if self.creators.count() < 1:
            return False
        # does it have any photos?
        if self.photo_set.count() < 1:
            return False
        # does it have any audio files?
        if self.audio_set.count() < 1:
            return False
        return True

    def as_geojson_feature(self, fields=None):
        # get the geojson representation of the feature
        location = self.location
        feature = location.as_geojson_feature_dict()
        feature['properties'] = model_to_dict(self, fields)
        if fields == None or 'description' in fields:
            asciibody = self.body.encode('utf-8')
            feature['properties']['description'] = asciibody
        feature['id'] = self.id
        return feature

class Question( DataModel, UUIDModel ):
    """A class for storing questions for interviews."""
    text_en = models.TextField()
    text_es = models.TextField( null=True, blank=True )

    def __unicode__(self):
        return self.text_en

class Photo( DataModel, UUIDModel ):
    """For storing photos related to interviews or users.
    """
    date_added = models.DateTimeField( auto_now_add=True )
    creators = models.ManyToManyField( 'UserProfile', null=True, blank=True )
    image = models.ImageField( upload_to=get_upload_path )
    interview = models.ForeignKey( 'Interview', null=True, blank=True )

    def __unicode__(self):
        return self.image.url

    def get_upload_path( self, filename ):
        return 'lottery/photos/%s' % filename

    def natural_key(self):
        return self.image.url

class Audio( DataModel, UUIDModel ):
    """for storing audio tracks from interviews."""
    date_added = models.DateTimeField( auto_now_add=True )
    interview = models.ForeignKey( 'Interview' )
    question = models.ForeignKey('Question', null=True, blank=True )
    file = models.FileField( upload_to=get_upload_path )

    def __unicode__(self):
        return self.file.url

    def get_upload_path( self, filename ):
        return 'lottery/audios/%s' % filename

class Quote( DataModel, UUIDModel ):
    """A model for storing quotes of Audio tracks."""
    date_added = models.DateTimeField( auto_now_add=True )
    date_edited = models.DateTimeField( auto_now=True )
    text = models.TextField()
    audio = models.ForeignKey('Audio')

    def __unicode__(self):
        return self.text

class Note( DataModel, UUIDModel ):
    """A model for storing text notes on questions."""
    date_added = models.DateTimeField( auto_now_add=True )
    date_edited = models.DateTimeField( auto_now=True )
    interview = models.ForeignKey( 'Interview' )
    question = models.ForeignKey('Question')
    text = models.TextField()

    def __unicode__(self):
        return self.text




