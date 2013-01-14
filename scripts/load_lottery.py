"""
A script for loading data for the lottery application

For copying data to another database, there are two options: using `pg_dump`
and using `python manage.py dumpdata`. `pg_dump` does a poor job of handling
foreignkeys, but `dumpdata` is slow for large amounts of data. None of them can
do forward referencing foreign keys to data that does not exist. The best
strategy seems to be to dump anything that has no foreign keys using `pg_dump`
and then dump the others using `dumpdata`.

"""
import os
import cPickle as pickle
import datetime
from subprocess import call # for pg_dump and command line

from django.contrib.gis.geos import Point
from django.contrib.auth.models import User

import xlrd
from datertots.core import (xls_to_dicts, writeToXls,
            csv_dictionaries, detect_encoding)
from scripts.nyc_zip import nyc_zips

from lottery.models import (
        Location, Retailer, SalesWeek, Win, Interview,
        Photo, UserProfile
        )
from geese.db import GeeseDB

from scripts.load_filters import cutoffs, replacers


# folder = "/Users/benjamin/Dropbox/CDDP/CityDigits/Lottery/01_DATA/raw_FOIA_data"
# agents = os.path.join( folder, "Changes of Ownership",
# "Foil-12001-019-Agents-unicode.csv" )
# changes = os.path.join( folder, "Changes of Ownership", "Foil-12001-019-Change-of-Ownerships.csv" )
# sales_folder = os.path.join( folder, "Sales Data" )
# sales_files = [os.path.join( sales_folder,
#     f) for f in os.listdir( sales_folder ) if '.csv' in f]
# 
# winnings_folder = os.path.join( folder, "Winnings Data" )
# winnings_files = [g for g in os.listdir( winnings_folder ) if ".xlsx" in g]
# winnings = [os.path.join(winnings_folder, h) for h in winnings_files]
# xls_folder = "/Users/benjamin/Dropbox/CDDP/CityDigits/Lottery/01_DATA/spreadsheets"
# sales_xls = os.path.join( xls_folder, "NYC_Sales-Aggregated_by_address.xls")
# corrections_xls = os.path.join( xls_folder, "retailer cleanup tables",
#                                             "notfound_location_corrections.xls")


def address_key( item, add_key ):
    """This function creates a composite string from several components of an
    object's address.
    """
    return '%s, %s, %s %s' % (
        item[add_key],
        item['city'],
        item['state'],
        item['zipcode'],
        )

def filter_address(address):
    for cutoff in cutoffs:
        if cutoff in address:
            index = address.find(cutoff)
            address = address[:index]
    for replacer in replacers:
        if replacer in address:
            new = replacers[ replacer ]
            address = address.replace( replacer, new )
    return address.strip()

def xls( filename, data, keys=None ):
    path = os.path.join( xls_folder, filename )
    writeToXls( path, data, keys )
    print 'wrote to %s' % filename

def write( filename, data ):
    path = os.path.join( os.path.split( folder )[0], "pickles", filename )
    f = open( path, 'wb' )
    pickle.dump( data, f )
    f.close()
    print 'wrote to %s' % filename

def read( filename ):
    folder = '/home/bengolder/webapps/citydigits/citydigits/lottery/sample_data/'
    path = os.path.join( folder, "pickles", filename )
    f = open( path, 'rb' )
    data = pickle.load( f )
    f.close()
    print 'read from %s' % filename
    return data

def load_locations(): # load these into django models and save them
    """Run First
        This extracts the addresses, and retailer IDs from the agent directory provided by NY
        Lotto.The addresses do not necessarily match the addresses that have
        been previously geocoded.
        It will only extract addresses with NY City zip codes.
    """
    # get raw locations
    rows = csv_dictionaries( agents )
    # make ny locations with raw locations
    retailers = {}
    locations = {}
    for agent in rows:
        if agent['BUSZIP'] in nyc_zips:
            raw_location = {
                    'street_address':agent['BUSADDR'],
                    'city':agent['BUSCITY'],
                    'state':'NY',
                    'zipcode':agent['BUSZIP'],
                    }
            full = address_key( raw_location, 'street_address' )
            raw_location['address'] = full

            # the key for locations is the full raw address
            if full not in locations:
                locations[full] = raw_location

            # the key for retailers is the agent number. And retailers retain
            # the full raw address.
            retailer = {
                    'name': agent['BUSNM'],
                    'retailer_id': agent['AGTNO'],
                    'location': full,
                    }
            retailers[ agent['AGTNO'] ] = retailer
    write( 'raw_ny_retailers', retailers )
    write( 'raw_ny_locations', locations )

def load_edited_addresses():# load these into django models and save them
    """Run Second
        This will take the raw addresses extracted in step one and filter them,
        using the address filters.
        It essentially copies all the raw locations, and stores them in a new
        dicitionary using their filtered address as a key.
    """
    locations = read( 'raw_ny_locations' )
    new_locs = {}
    for k in locations:
        loc = locations[k]
        old = loc['street_address']
        new = filter_address( old )
        loc['filtered_address'] = new
        newkey = address_key( loc, 'filtered_address' )
        new_locs[newkey] = loc
    write( 'filtered_ny_locations', new_locs )

def load_points(): # load these into django models and save them
    """Run Third
        This compares the filtered addresses to the previously geocoded points,
        in order to determine the lat lng of each location.  It simply records
        what was and was not found. Ater this step it is necessary to correct
        the addresses that did not match. The resulting corrections can be found
        in the file 'notfound_location_corrections.xls'.
    """
    # locations are the listed locations
    locations = read( 'filtered_ny_locations' )

    # sales are the sales locations
    sales = xls_to_dicts( sales_xls )

    not_found = {}
    found = {}
    for row in sales:
        add = row['address']
        if add in locations:
            print 'FOUND: %s' % add
            locations[add]['lat'] = row['lat']
            locations[add]['lng'] = row['lng']
            found[add] = locations[add]
        else:
            print 'NOT FOUND: %s' % add
            not_found[add] = {
                    'address': add,
                    'street_address':row['street_address'],
                    'city':row['city'],
                    'state':row['state'],
                    'zipcode':row['zipcode'],
                    'name':row['name'],
                    }
    write( 'found_ny_locations', found )
    write( 'notfound_ny_locations', not_found )
    xloc = [locations[k] for k in locations]
    keys = xloc[0].keys()
    keys.extend( ['lat', 'lng'] )
    xfound = [found[k] for k in found]
    xnot_found = [not_found[k] for k in not_found]
    xls( 'all_locations.xls', xloc, keys )
    xls( 'found_ny_locations.xls', xfound )
    xls( 'notfound_ny_locations.xls', xnot_found )
    r = read( 'raw_ny_retailers' )
    sellers = [r[k] for k in r]
    xls( 'retailers.xls', sellers )

def repair_points():
    """
    What it should do now that I have corrections.
        if the address is not found:
            look in the list of not_found locations
            get the listed_address
            use that to look up the listed location
            treat it as found
    """
    locations = read( 'filtered_ny_locations' )
    sales = xls_to_dicts( sales_xls )
    corrections = xls_to_dicts( corrections_xls )
    for row in sales:
        add = row['address']
        street_add = row['street_address']
        # deal with the broken ones
        if add not in locations:
            # find the correction
            corrected = find_dict( street_add, corrections, 'sales_address' )
            if not corrected:
                print add
            location = locations[corrected['listed_address']]
        else:
            location = locations[add]
        # make the point and location objects
        point = Point( row['lng'], row['lat'] )
        loc = Location()
        loc.point = point
        # use the address information from sales, not from the retailer
        # listings, because these are the addresses that were geocoded
        loc.address_text = add
        loc.raw_address_text = location['address']
        loc.street_address = street_add
        loc.city = row['city']
        loc.state = 'NY'
        loc.zipcode = int(row['zipcode'])
        # save the new location object
        loc.save()

def add_retailers():
    retailers_db = read( 'raw_ny_retailers' )
    retailers = [retailers_db[k] for k in retailers_db]
    # look up the location for each retailer
    for retailer in retailers:
        # use the raw address for this location to lookup the retailer
        raw_address = retailer['location']
        try:
            location = Location.objects.get(raw_address_text=raw_address)
        except:
            print "couldn't find %s" % retailer['name']
            location = None
        if location:
            print 'found %s at %s' % (retailer['name'], location)
            retail = Retailer()
            retail.location = location
            retail.name = retailer['name']
            retail.retailer_id = retailer['retailer_id']
            retail.save()
            print 'saved'

def load_winnings():
    """open and read winnings data and load it into the database
        The winnings records contain address components as well as retailer ids
        but this will only use the retailer ids and will not load the addresses
        from the winnings
    """
    root = '/home/bengolder/webapps/citydigits/citydigits/lottery/sample_data/'
    folder = os.path.join(root, 'xls')
    winfiles = [n for n in os.listdir(folder) if n[-4:] == '.xls']
    winnings = [os.path.join(folder, w) for w in winfiles]
    for f in winnings:
        new_wins = xls_to_dicts(f, column_to_datetime='Date Won/Claimed')
        for win in new_wins:
            retailer_id = str(int(win['Ret #']))
            try:
                retailer = Retailer.objects.get(retailer_id=retailer_id)
            except:
                retailer = None
            if retailer:
                print 'found at %s' % retailer
                date = win['Date Won/Claimed']
                amount = win['Prize']
                game = win['Game Name']
                win_obj = Win()
                win_obj.retailer = retailer
                win_obj.date = date
                win_obj.amount = amount
                win_obj.game = game
                win_obj.save()
                print 'saved'

def repair_sales():
    """This function links sales to a retailer with a specific retailer ID.
        It uses the listed address in the sales data to look up a location.
        with that location, it finds all the retailers associated with the
        location. Using the retailer name listed in the sales data, it tries to
        find a retailer associated with the location.
        retailer and address combinations that cannot be found (and thus do not
        match other data supplied by NY Lottery) are written to a separate
        excel file.
    """
    bad_addresses = []
    bad_names = []
    for sales_file in sales_files:
        fields = ('name','street_address','city','zipcode','date','amount')
        iterator = csv_dictionaries( sales_file, fields )
        for row in iterator:
            if int(row['zipcode']) in nyc_zips:
                # filter street address to match filtered addresses
                row['street_address'] = filter_address( row['street_address'] )
                row['amount'] = float(row['amount'])
                row['state'] = 'NY'
                # create address key for location lookup
                key = address_key( row, 'street_address')
                # search for location
                loc_results = Location.objects.filter(address_text=key)
                # if not found, store object in bad_address list
                if not loc_results or len(loc_results) > 1:
                    bad_addresses.append( row )
                else:
                    location = loc_results[0]
                    # if found, search location retailers for retailer name
                    retailers = location.retailer_set.filter(name=row['name'])
                    # if no retailer found, store in bad_name list
                    if not retailers or len(retailers) > 1:
                        bad_names.append(row)
                    else:
                        # otherwise, create a sales week object,
                        saleswk = SalesWeek()
                        saleswk.retailer = retailers[0]
                        saleswk.amount = row['amount']
                        datetext = row['date']
                        # don't forget to convert the date.
                        date = datetime.datetime.strptime(datetext, '%Y-%m-%d')
                        saleswk.week = date
                        # save it
                        saleswk.save()
    # write the failures to excel files
    xls('sales-bad_address.xls', bad_addresses)
    xls('sales-bad_names.xls', bad_names)

def find_dict( val, others, key ):
    """A function to match a dictionary to another out of a list, based on the
    value of a particular key.
    """
    for other in others:
        if other[key] == val:
            return other

def load_interviews():
    """load sample interviews"""
    folder = 'lottery/sample_data/interviews'
    interview_files = [f for f in os.listdir( folder ) if f[-4:]=='.txt']
    for interview_file in interview_files:
        path = os.path.join(folder, interview_file)
        text = open(path, 'r').read()
        interviewer = interview_file.split('_')[0]
        interview = Interview()
        interview.slug = os.path.splitext(interview_file)[0]
        interview.body = text
        interview.save()

def load_photos():
    """load sample interview pictures
    """
    folder = 'lottery/sample_data/photos'
    photo_files = [f for f in os.listdir( folder ) if f[-4:]=='.jpg']
    for photo_file in photo_files:
        path = os.path.listdir(folder, photo_file)

def load_sample_users():
    """load the file of sample users.
    """
    path = 'lottery/sample_data/users.txt'
    f = open(path, 'r')
    for line in f:
        full_name, email = tuple([t.strip() for t in line.split(',')])
        password = email.split('@')[0]
        user = User.objects.create_user(password, email, password)
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.name = full_name
        profile.save()

def dump_locations():
    folder = 'lottery/sample_data/'
    db = GeeseDB()
    table = 'lottery_location'
    path = os.path.join( folder, '%s.csv' % table )
    db.layer_to_csv( table, path, exclude=['id'] )


def read_locations():
    home = '/home/bengolder/webapps/citydigits/'
    folder = 'citydigits/lottery/sample_data/'
    db = GeeseDB()
    table = 'lottery_location'
    path = os.path.join( home, folder, '%s.csv' % table )
    db.csv_to_layer( table, path )

def django_file():
    import django
    print django.__file__

################# Run things ###################
#load_locations()
#load_edited_addresses()
#load_points( )
#repair_points()
#add_retailers()
#load_winnings()
#repair_sales()
#load_interviews()
#load_photos()
#read_locations()
django_file()

print "\a"
print "\a"
print "\a"

