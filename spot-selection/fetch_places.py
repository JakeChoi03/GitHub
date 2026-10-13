"""Collect tourist places around a centre point with the Google Places API (New).

Writes <area>/unique.json in the same shape as the Asakusa Apify data
(title, categoryName, reviewsCount, totalScore, lat, lng, permanentlyClosed,
temporarilyClosed), so build.py / select.py / map.py can be reused.

Usage: GOOGLE_MAPS_API_KEY=... python3 fetch_places.py ueno|toyosu|harajuku|all
"""
import json
import math
import os
import sys
import time
import urllib.request

AREAS = {
    # name: (lat, lng) of the centre; radius 1.5 km, same as Asakusa
    'ueno': (35.7190, 139.7700),      # Ueno-Yanaka-Nezu
    'toyosu': (35.6530, 139.7880),
    'harajuku': (35.6702, 139.7027),
}
RADIUS_M = 1500
QUERIES = ['tourist attraction', 'temple', 'shrine', 'museum', 'park',
           'shopping street', 'souvenir shop']
FIELDS = ','.join(['places.id', 'places.displayName', 'places.primaryTypeDisplayName',
                   'places.userRatingCount', 'places.rating', 'places.location',
                   'places.businessStatus', 'nextPageToken'])
URL = 'https://places.googleapis.com/v1/places:searchText'


def haversine(a, b, c, d):
    p = math.radians
    x = math.sin(p(c - a) / 2) ** 2 + math.cos(p(a)) * math.cos(p(c)) * math.sin(p(d - b) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(x))


def quadrants(lat, lng):
    # Text Search returns at most 60 results per query, so search 4 quadrants of the circle's bounding box
    dlat = RADIUS_M / 110574
    dlng = RADIUS_M / (111320 * math.cos(math.radians(lat)))
    for la0, la1 in ((lat - dlat, lat), (lat, lat + dlat)):
        for lo0, lo1 in ((lng - dlng, lng), (lng, lng + dlng)):
            yield {'rectangle': {'low': {'latitude': la0, 'longitude': lo0},
                                 'high': {'latitude': la1, 'longitude': lo1}}}


def search(key, query, restriction):
    token, out = None, []
    for _ in range(3):  # 3 pages x 20 = 60 max
        body = {'textQuery': query, 'locationRestriction': restriction, 'languageCode': 'en', 'pageSize': 20}
        if token:
            body['pageToken'] = token
        req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={
            'Content-Type': 'application/json', 'X-Goog-Api-Key': key, 'X-Goog-FieldMask': FIELDS})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        out += data.get('places', [])
        token = data.get('nextPageToken')
        if not token:
            break
        time.sleep(2)
    return out


def fetch(area, key):
    lat, lng = AREAS[area]
    places, calls = {}, 0
    for q in QUERIES:
        for rect in quadrants(lat, lng):
            for p in search(key, q, rect):
                places[p['id']] = p
            calls += 1
    rows = []
    for p in places.values():
        la, lo = p['location']['latitude'], p['location']['longitude']
        if haversine(lat, lng, la, lo) > RADIUS_M:
            continue
        rows.append({
            'title': p.get('displayName', {}).get('text', ''),
            'categoryName': p.get('primaryTypeDisplayName', {}).get('text', ''),
            'reviewsCount': p.get('userRatingCount', 0),
            'totalScore': p.get('rating'),
            'lat': la, 'lng': lo,
            'permanentlyClosed': p.get('businessStatus') == 'CLOSED_PERMANENTLY',
            'temporarilyClosed': p.get('businessStatus') == 'CLOSED_TEMPORARILY',
            'placeId': p['id'],
        })
    os.makedirs(area, exist_ok=True)
    with open(os.path.join(area, 'unique.json'), 'w') as f:
        json.dump(rows, f, ensure_ascii=False)
    print(f'{area}: {len(rows)} places within {RADIUS_M} m ({calls} query-quadrants)')


if __name__ == '__main__':
    key = os.environ.get('GOOGLE_MAPS_API_KEY')
    if not key:
        sys.exit('GOOGLE_MAPS_API_KEY is not set')
    targets = list(AREAS) if sys.argv[1:] == ['all'] else sys.argv[1:]
    for a in targets:
        fetch(a, key)
