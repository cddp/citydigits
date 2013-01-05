import os
import cPickle as pickle

from datertots.core import (xls_to_dicts, writeToXls,
            csv_dictionaries, detect_encoding)
from datertots.nyc_zip import nyc_zips
from load_filters import cutoffs, replacers




folder = "/Users/benjamin/Dropbox/CDDP/CityDigits/Lottery/01_DATA/raw_FOIA_data"
agents = os.path.join( folder, "Changes of Ownership",
"Foil-12001-019-Agents-unicode.csv" )
changes = os.path.join( folder, "Changes of Ownership", "Foil-12001-019-Change-of-Ownerships.csv" )
sales_folder = os.path.join( folder, "Sales Data" )
sales_files = [os.path.join( sales_folder,
    f) for f in os.listdir( sales_folder ) if '.csv' in f]

winnings_folder = os.path.join( folder, "Winnings Data" )
winnings_files = [g for g in os.listdir( winnings_folder ) if ".xlsx" in g]
xls_folder = "/Users/benjamin/Dropbox/CDDP/CityDigits/Lottery/01_DATA/spreadsheets"
sales_xls = os.path.join( xls_folder, "NYC_Sales-Aggregated_by_address.xls")


def address_key( item, add_key ):
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
    path = os.path.join( os.path.split( folder )[0], "pickles", filename )
    f = open( path, 'rb' )
    data = pickle.load( f )
    f.close()
    print 'read from %s' % filename
    return data


def load_locations():
    """Run First"""
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
            # store location
            if full not in locations:
                locations[full] = raw_location
            retailer = {
                    'name': agent['BUSNM'],
                    'retailer_id': agent['AGTNO'],
                    'location': full,
                    }
            retailers[ agent['AGTNO'] ] = retailer
    write( 'raw_ny_retailers', retailers )
    write( 'raw_ny_locations', locations )

def load_edited_addresses():
    """Run Second"""
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

def load_points():
    """Run Third"""
    locations = read( 'filtered_ny_locations' )
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


def load_interviews():
    # get the interviews from the sample data
    pass

def load_photos():
    # get the photos from the sample data
    pass

def load_winnings():
    # get the winnings from the raw data
    pass

if __name__=='__main__':
    #load_locations()
    #load_edited_addresses()
    load_points( )



