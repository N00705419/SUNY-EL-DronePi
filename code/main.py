import camera
from gps import *
from time import *
import threading
import time
import datetime
import database
import os
import csv
#import GpsPoller


camera = camera.Camera()
#gps = gpsPi.Gps()
db = database.Database('../www/database/pi_database.db')

gpsd = None

os.system('clear')

# camera
def triggerCamera(gpsData):

    gpsCoordinatesOptions = ""

    dateString = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    #gpsDataFormated = formatGpsData(gpsData)

    # this section should be uncomented when the method formatGpsData is working
    # if gpsData:
    #     gpsCoordinatesOptions = (
    #     " --exif GPS.GPSLatitude=%s "
    #     " --exif GPS.GPSLongitude=%s "
    #     " --exif GPS.GPSAltitude=%s "
    #     ) % ( gpsDataFormated['latitude'], gpsDataFormated['longitude'], gpsDataFormated['altitude'])
    # else:
    #     print "ERROR: gpsData is empty"
    #     os.system( "echo 'ERROR: gpsData is empty' %s >> log.txt" % (dateString))

    cameraOptions = (
                    " --exposure sports "
                    " --width 800 "
                    " --height 600 "
                    " --quality 75 "
                    " --verbose "
                    " --nopreview "
                    )

    options = cameraOptions + gpsCoordinatesOptions

    fullPath = 'http://drone.nulldivision.com/www/images/camera/'
    fileName = dateString + '.jpg'

    dataToDatabase = {
        'dateTime': dateString,
        'pathToImage': fullPath + fileName,
        'latitude': gpsData['latitude'],
        'longitude': gpsData['longitude'],
        'altitude': gpsData['altitude']
    }

    pathToImage = '../www/images/camera/' + fileName
    db.dataEntry(dataToDatabase)

    try:
        camera.takePicture(options, pathToImage)
    except Exception, e:
        dateString = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        os.system( "echo 'ERROR: picture NOT saved' %s >> log.txt" % (dateString))
    else:
        db.dataEntry(dataToDatabase)
        return 1


# TODO format lat and lon
# def formatGpsData(gpsData):
    # Receives the latitude, longitude and altitude with the original format from gps reading
    # And converts to the camera options required format
    # Required format sample: latitude or longitude: '-33/1,66/1,451/100' Altitude: 71.2/10
    # gpsDataFormated = {}
    # gpsDataFormated['latitude'] = gpsData['latitude']
    # gpsDataFormated['longitude'] = gpsData['longitude']
    # gpsDataFormated['altitude'] = gpsData['altitude'] + '/10'
    # return gpsDataFormated

def getMission(pathToFile = 'mission.txt'):
    # reads from the file exported from mission control and parses the latitude, longitude and altitude to a list
    with open(pathToFile) as f:
        reader = csv.reader(f, delimiter="\t")
        fileMission = list(reader)

    fileMissionLength = len(fileMission) - 1
    # mission is an array of dictionaries
    mission = dictlist = [dict() for x in range(fileMissionLength - 1)]

    for x in range(2, fileMissionLength + 1):
        mission[x - 2]['latitude'] = float(fileMission[x][8])
        mission[x - 2]['longitude'] = float(fileMission[x][9])
        mission[x - 2]['altitude'] = float(fileMission[x][10])

    return mission

def isInsideRange(gpsData, coordinatesRange, mission):
    #verifies if the gpsData is inside a squared range built with the waipoint coordinates plus a range pre determined by the user
    for waypoint in mission:

        # if (gpsData['altitude'] > 5.0):
        if( gpsData['latitude'] < waypoint['latitude'] + coordinatesRange and
            gpsData['latitude'] > waypoint['latitude'] - coordinatesRange):

            if( gpsData['longitude'] < waypoint['longitude'] + coordinatesRange and
                gpsData['longitude'] > waypoint['longitude'] - coordinatesRange):

                print ("Waypoint reached:")
                print (waypoint)
                mission.remove(waypoint)
                print ("Waypoint removed from list")
                return True
            else:
                return False
        else:
            return False


class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd
        gpsd = gps(mode=WATCH_ENABLE)
        self.current_value = None
        self.running = True

    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next()


if __name__ == '__main__' :

    gpsp = GpsPoller()
    coordinatesRange = 0.0001
    mission = getMission()

    try:
        gpsp.start()
        while True:
            os.system('clear')
            gpsData = {'latitude' : gpsd.fix.latitude, 'longitude': gpsd.fix.longitude, 'altitude' : gpsd.fix.altitude}

            print('Reading gps')
            print(gpsData)

            if (isInsideRange(gpsData, coordinatesRange, mission)):
                print ("Waiting for drone to stabilize")
                time.sleep(10)
                try:
                    triggerCamera(gpsData)
                    print("Waiting for picture to be taken")
                    time.sleep(15)
                except Exception, e:
                    print "Range error:", sys.exc_info()[0]
                else:
                    print "Successful Waypoint"

    except (KeyboardInterrupt, SystemExit):
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join()
        print "Done. \nExiting."
