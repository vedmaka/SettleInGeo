# -*- coding: utf-8 -*-

#import pycountry
#import xml.etree.ElementTree
import unicodedata
import pymysql.cursors
import re

import mwclient

def pp( str ):
    str = unicodedata.normalize( 'NFC', str ).encode('ascii', 'ignore').decode('utf-8')
    str = re.sub("[']", "", str)
    return str

connection = pymysql.connect(host='localhost',
                             user='vedmaka',
                             password='',
                             db='c9',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                             
site = mwclient.Site( ('http', 'settlein.org') , '/')
site.login('admin','q1w2e3r4')

countryValues = []
stateValues = []
cityValues = []

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `sortname`, `name` FROM `countries`"
        cursor.execute(sql)
        result = cursor.fetchone()
        while result is not None:
            # Country: ---------------------------------------------------------
            print(pp(result['name']))
            countryValues.append( pp(result['name']) )
            # Fetch states
            with connection.cursor() as cursor2:
                sql = "SELECT * FROM `states` WHERE country_id = " + str(result['id'])
                cursor2.execute(sql)
                result2 = cursor2.fetchone()
                while result2 is not None:
                    # State: ---------------------------------------------------
                    print("\t -" + pp(result2['name']))
                    stateValues.append( pp(result2['name']) )
                    # Fetch citites
                    with connection.cursor() as cursor3:
                        sql = "SELECT * FROM `cities` WHERE state_id = " + str(result2['id'])
                        cursor3.execute(sql)
                        result3 = cursor3.fetchone()
                        while result3 is not None:
                            # City: --------------------------------------------
                            print("\t\t -" + pp(result3['name']))
                            cityValues.append( pp(result3['name']) )
                            result3 = cursor3.fetchone()
                    result2 = cursor2.fetchone()
            result = cursor.fetchone()
        
finally:
    connection.close()

# Countries
countryText = "[[has type::Text]]\n"
for country in countryValues:
    countryText = countryText + "\n* [[Allows value::" + country + "]]"

p = site.Pages['Property:Country']
p.save( countryText, summary = 'Geo script' )

# States
stateText = "[[has type::Text]]\n"
for state in stateValues:
    stateText = stateText + "\n* [[Allows value::" + state + "]]"

p = site.Pages['Property:State']
p.save( stateText, summary = 'Geo script' )

# Cities
cityText = "[[has type::Text]]\n"
for city in cityValues:
    cityText = cityText + "\n* [[Allows value::" + city + "]]"

p = site.Pages['Property:City']
p.save( cityText, summary = 'Geo script' )