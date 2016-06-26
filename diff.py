# -*- coding: utf-8 -*-

import pymysql.cursors
import difflib
import mwclient

connection = pymysql.connect(host='localhost',
                             user='vedmaka',
                             password='',
                             db='c9',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                  
countries = []         

try:
    with connection.cursor() as cursor:
        # Read countries
        sql = "SELECT `id`, `sortname`, `name` FROM `countries`"
        cursor.execute(sql)
        result = cursor.fetchone()
        while result is not None:
            countries.append( result['name'].lower() )
            result = cursor.fetchone()
finally:
    connection.close()
    
matching_countries = difflib.get_close_matches('rossiya', countries)
confidence = difflib.SequenceMatcher(None, matching_countries[0], 'rossiya').quick_ratio()

print("Confidence: %s" % confidence)
print("----------------------------")
print(matching_countries)

site = mwclient.Site('testing-cloud-9-ide-1-vedmaka.c9users.io', '/')
site.login('admin','q1w2e3r4')
