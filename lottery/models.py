from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from citydigits.settings import MEDIA_ROOT
from geese.models import GeeseModel
from datertots.models import  DataModel, UUIDModel

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

class Location( GeeseModel,  DataModel ):
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

class Question( DataModel, UUIDModel ):
    """A class for storing questions for interviews."""
    text = models.TextField()
    text_es = models.TextField( null=True, blank=True )

    def __unicode__(self):
        return self.text

class Interview( GeeseModel, DataModel, UUIDModel ):
    """A class for storing information about interviews."""
    point = models.PointField()
    description = models.CharField( max_length=300 )
    date_added = models.DateTimeField( auto_now_add=True )
    date_edited = models.DateTimeField( auto_now=True )
    creators = models.ManyToManyField( 'UserProfile', null=True, blank=True )

    def __unicode__(self):
        return self.slug

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

class Photo( DataModel, UUIDModel ):
    """For storing photos related to interviews or users.
    """
    date_added = models.DateTimeField( auto_now_add=True )
    creators = models.ManyToManyField( 'UserProfile', null=True, blank=True )
    image = models.ImageField( upload_to=get_upload_path )
    interview = models.ForeignKey( 'Interview', null=True, blank=True )

    def get_upload_path( self, filename ):
        return 'lottery/photos/%s' % filename

    def natural_key(self):
        return self.image.url

class Audio( DataModel, UUIDModel ):
    """for storing audio tracks from interviews."""
    interview = models.ForeignKey( 'Interview' )
    question = models.ForeignKey('Question', null=True, blank=True )
    file = models.FileField( upload_to=get_upload_path )

    def get_upload_path( self, filename ):
        return 'lottery/audios/%s' % filename

    class Meta:
        abstract=True

class Quote( DataModel, UUIDModel ):
    """A model for storing quotes of Audio tracks."""
    text = models.TextField()
    audio = models.ForeignKey('Audio')

    class Meta:
        abstract=True




