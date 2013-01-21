from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from citydigits.settings import MEDIA_ROOT
from geese.models import GeeseModel
from datertots.models import  DataModel

def get_upload_path(instance, filepath):
    return instance.get_upload_path(filepath)

class UserProfile( DataModel ):
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

class Retailer( DataModel):
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

class SalesWeek( DataModel):
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

class InterviewManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

class Interview( DataModel ):
    """A class for storing information about interviews."""
    slug = models.SlugField()
    date_added = models.DateTimeField( auto_now_add=True )
    date_edited = models.DateTimeField( auto_now=True )
    creators = models.ManyToManyField( 'UserProfile', null=True, blank=True )
    body = models.TextField( null=True, blank=True )
    location = models.ForeignKey( 'Location', null=True, blank=True )
    process_as = models.CharField( max_length=50, default="markdown",
            null=True, blank=True )

    objects = InterviewManager()

    def __unicode__(self):
        return self.slug

    def natural_key(self):
        return self.slug

    def as_geojson_feature(self, fields=None):
        # get the geojson representation of the feature
        location = self.location
        feature = location.as_geojson_feature_dict()
        feature['properties'] = model_to_dict(self, fields)
        feature['properties']['location_id'] = location.id
        if fields == None or 'body' in fields:
            asciibody = self.body.encode('utf-8')
            feature['properties']['body'] = asciibody
        feature['id'] = self.id
        return feature

def interviews_locations():
    return Interview.objects.select_related()

class Photo( DataModel ):
    """For storing photos related to interviews or users.
    """
    date_added = models.DateTimeField( auto_now_add=True )
    creators = models.ManyToManyField( 'UserProfile', null=True, blank=True )
    image = models.ImageField( upload_to=get_upload_path )
    interview = models.ForeignKey( 'Interview', null=True, blank=True )
    location = models.ForeignKey( 'Location', null=True, blank=True )
    caption = models.TextField( null=True, blank=True )

    def get_upload_path( self, filename ):
        return 'lottery/photos/%s' % filename

    def natural_key(self):
        return self.image.url

class AudioFile( DataModel ):
    """for storing audio interviews"""
    pass
    class Meta:
        abstract=True

class Borough( DataModel ):
    """For storing the 5 boroughs"""
    pass
    class Meta:
        abstract=True

class Neighborhood( DataModel ):
    """For storing the different neighborhoods"""
    pass
    class Meta:
        abstract = True

class BlockGroup( DataModel ):
    """For storing block group data """
    pass
    class Meta:
        abstract = True



