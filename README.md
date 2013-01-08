# citydigits.org

This is a repo for the citydigits website.


## URL Scheme 

Each of these correponds to a view function in either
citydigts/views.py or lottery/views.py (#) = any number less than the number of objects

    http://citydigits.org/
        admin/ - the admin interface for adding/editing data
            doc/ - automatic documentation for the code
        login/ - gets you to the login form
        lottery/ - lottery project home page
            about/ - lottery about page
            interviews/ - the photo-grid page
                (#)/ - interview detail
            map/ - interview map
                (#)/ - interview map highlight
            map-split/(#)/ - interview map/detail split
            data/ - data explorer
            tutorial/ - tutorial for the public
            user-tutorial/ - tutorial for students
            --- proposed ---
            fieldwork/ - url for students in the field
            

## HTML Templates

    citydigits/templates/
        base.html - the base template that all pages inherit from
        registration/
            login.html - the login page
            login_form.html - the login form
        lottery/
            about.html - template for about page
            data_explorer.html - template for data explorer home
            interview_detail.html - template for interview detail view
            interview_list.html - template for a plain list of interviews
            interview_map.html - template for interview map view
            interview_map_detail.html - template for map highlight view
            interview_photo_grid.html - template for photo grid view
            interview_split.html - template for map split view
            pull_down_intro.html - the introductory text that appears on the left side of the pull-down menu
            public_pull_down_menu.html - the template for the pull-down menu
            js/ - javascript templates
            svg/ - graphics/icons templates
            forms/
                photo_form.html - template for the photo upload form

## Models

lottery/models.py

__UserProfile__ - this is for storing any additional details about users

* name - full name of this user
* user - link to the user pbject for this profile

__Location__ - for a specific point in space, including address

* point - the point in space
* address_text - full address text from sales data
* street_address
* raw_street_address - full address text from retailer listings
* city
* state
* zipcode

__Retailer - for a lottery retailer__

* name
* retailer_id
* location
    
__SalesWeek__

* week
* amount
* retailer

__Win__

* date
* retailer
* amount
* game

__Interview__

* slug
* date_added
* date_edited
* creators
* body
* location

__Photo__

*  date_added
*  creators
*  image
*  interview
*  location
*  caption 

__AudioFile__

__Borough__

__Neighborhood__

__BlockGroup__

