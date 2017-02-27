import pyrebase
from config import FIREBASE_CONFIG
from app import geo

from app.constants import locationsTable, venuesTable, GPS_LOCATIONS

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)

# The casing of tripadvisor is not consistent across our Firebase scripts
TA_PROVIDER = "tripadvisor"
TA_DETAILS = "tripAdvisor"

dryRun = True

def updateStatus(center, radius_km, provider, detailsProvider, version):
    location_table = firebase.database().child(locationsTable).get().val()
    placeIDs = geo.get_place_ids_in_radius(center, radius_km, location_table)
    print("number found {}".format(len(placeIDs)))

    statusTable = firebase.database().child(venuesTable, "status").get().val()
    placeDetails = firebase.database().child(venuesTable, "details").get().val()

    count = 0
    placeList = []
    for placeID in placeIDs:
        providers = placeDetails[placeID]["providers"]
        if detailsProvider in providers and statusTable[placeID][provider] == -1:
            count += 1
            st = firebase.database().child(venuesTable, "status", placeID)
            if not dryRun:
                st.update({provider: version})
            placeList.append(placeID)

    placeList.sort()
    print("Places updated: {}".format(placeList))
    print("total {} places with details: {}".format(detailsProvider, count))

if __name__ == '__main__':
    updateStatus(GPS_LOCATIONS["CHICAGO_CENTER"], 30, TA_PROVIDER, TA_DETAILS, 3)
