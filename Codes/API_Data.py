import http.client
import json
import pprint

connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X-Auth-Token': '75d1c50b4fae4bef90e35672c702bbc0',
           'X-Response-Control': 'minified'}
connection.request('GET', '/v1/competitions', None, headers)
response = json.loads(connection.getresponse().read().decode())

pprint.pprint(response)