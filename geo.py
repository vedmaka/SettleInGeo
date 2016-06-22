#import pycountry
#import xml.etree.ElementTree
import unicodedata
import pymysql.cursors

def pp( str ):
    return unicodedata.normalize( 'NFC', str ).encode('ascii', 'ignore').decode('utf-8')

connection = pymysql.connect(host='localhost',
                             user='vedmaka',
                             password='',
                             db='c9',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `sortname`, `name` FROM `countries`"
        cursor.execute(sql)
        result = cursor.fetchone()
        while result is not None:
            print(result['name'])
            # Fetch states
            with connection.cursor() as cursor2:
                sql = "SELECT * FROM `states` WHERE country_id = " + str(result['id'])
                cursor2.execute(sql)
                result2 = cursor2.fetchone()
                while result2 is not None:
                    print("\t -" + result2['name'])
                    # Fetch citites
                    with connection.cursor() as cursor3:
                        sql = "SELECT * FROM `cities` WHERE state_id = " + str(result2['id'])
                        cursor3.execute(sql)
                        result3 = cursor3.fetchone()
                        while result3 is not None:
                            print("\t\t -" + result3['name'])
                            result3 = cursor3.fetchone()
                    result2 = cursor2.fetchone()
            result = cursor.fetchone()
        
finally:
    connection.close()

'''
for country in pycountry.countries:
    print( pp(country.name) + " (" + country.alpha2 + ")")
    subs = None
    try:
        subs = pycountry.subdivisions.get(country_code=country.alpha2)
    except:
        subs = None
    if subs is not None:
        for subdiv in subs:
            print("\t- " + pp(subdiv.name) + " | " + subdiv.type)
            pr = None
            try:
                pr = subdiv.parent
            except:
                pr = None
            if pr is not None:
                print("\t\t- parent: " + pp(pr.name) + " | " + pr.type)
'''

'''
e = xml.etree.ElementTree.parse('geonames.xml').getroot()
start = e.find('Children')
for item in start:
    print(pp(item.find('Name').text))
    sub = item.find('Children')
    if sub is not None:
        for subItem in sub:
            print("\t -" + pp(subItem.find('Name').text))
            states = subItem.find('Children')
            if states is not None:
                for state in states:
                    print("\t\t -" + pp(state.find('Name').text))
'''