from django.contrib.gis.db import models

def get_upload_path(instance, filepath):
    return instance.get_upload_path(filepath)

class UserProfile( models.Model ):
    """This class should store information about a user who uploads interviews.
    """
    name = models.CharField( max_length=500 )
    def __unicode__(self):
        return self.name
    class Meta:
        abstract = True

class Location( models.Model ):
    """For storing the locations, of retailers or interviews."""
    latitude = models.FloatField( null=True, blank=True )
    longitude = models.FloatField( null=True, blank=True )
    address_text = models.TextField( null=True, blank=True )
    street_address = models.CharField( max_length=500, null=True, blank=True )
    city = models.CharField( max_length=100, null=True, blank=True )
    state = models.CharField( max_length=100, null=True, blank=True )
    zipcode = models.CharField( max_length=100, null=True, blank=True )

    def __unicode__(self):
        if self.latitude:
            return '%s, %s' % ( self.longitude, self.latitude )
        else:
            return self.address_text

    def coord(self):
        return self.longitude, self.latitude

class Retailer( models.Model):
    """For storing distinct retailer names and retailer IDs
    """
    name = models.CharField( max_length = 500 )
    retailer_id = models.CharField( max_length = 100 )
    location = models.ForeignKey( 'Location', null=True, blank=True )
    def __unicode__(self):
        return '%s: %s' % ( self.retailer_id, self.name )
    class Meta:
        abstract = True

class SalesWeek( models.Model):
    """For storing one week of sales at a particular place.
    """
    week = models.DateField()
    amount = models.FloatField()
    retailer = models.ForeignKey( 'Retailer' )
    class Meta:
        abstract = True

class Win( models.Model ):
    """For storing a winning ticket.
    """
    date = models.DateField()
    retailer = models.ForeignKey( 'Retailer ')
    amount = models.FloatField()
    game = models.CharField( max_length=300 )
    class Meta:
        abstract = True

class Interview( models.Model ):
    """A class for storing information about interviews."""
    slug = models.SlugField()
    date_added = models.DateTimeField( auto_now_add=True )
    date_edited = models.DateTimeField( auto_now=True )
    #creators = models.ManyToManyField( 'UserProfile', null=True, blank=True )
    body = models.TextField( null=True, blank=True )
    location = models.ForeignKey( 'Location', null=True, blank=True )

    #def markup

class Photo( models.Model ):
    """For storing photos related to interviews or users."""
    date_added = models.DateTimeField( auto_now_add=True )
    creators = models.ManyToManyField( 'UserProfile', null=True, blank=True )
    image = models.ImageField( upload_to = get_upload_path )
    interview = models.ForeignKey( 'Interview', null=True, blank=True )
    #user = models.ForeignKey( 'UserProfile', null=True, blank=True )
    caption = models.TextField( null=True, blank=True )

    def get_upload_path( self, filename ):
        return 'lottery/photos/%s' % filename

class AudioFile( models.Model ):
    """for storing audio interviews"""
    pass
    class Meta:
        abstract=True

class Borough( models.Model ):
    """For storing the 5 boroughs"""
    pass
    class Meta:
        abstract=True

class Neighborhood( models.Model ):
    """For storing the different neighborhoods"""
    pass
    class Meta:
        abstract = True

class BlockGroup( models.Model ):
    """For storing block group data """
    pass
    class Meta:
        abstract = True



