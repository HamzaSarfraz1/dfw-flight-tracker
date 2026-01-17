AVIATION_API_KEY = "0c1fad3977a3b907076ec014cbb4cf4e"

BASE_URL = "http://api.aviationstack.com/v1/flights"

DOMESTIC_ROUTES = [
    {"from": "DFW", "to": "LAX", "name": "DFW to Los Angeles", "type": "domestic"},
    {"from": "DFW", "to": "JFK", "name": "DFW to New York", "type": "domestic"},
    {"from": "DFW", "to": "ORD", "name": "DFW to Chicago", "type": "domestic"}
]

INTERNATIONAL_ROUTES = [
    {"from": "DFW", "to": "LHR", "name": "DFW to London", "type": "international"},
    {"from": "DFW", "to": "MEX", "name": "DFW to Mexico City", "type": "international"}
]

DATA_FOLDER = "data"