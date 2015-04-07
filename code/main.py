import camera
from gps import *
from time import *
import threading
import time
import datetime
import database
import os
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
def formatGpsData(gpsData):
    # Receives the latitude, longitude and altitude with the original format from gps reading
    # And converts to the camera options required format
    # Required format sample: latitude or longitude: '-33/1,66/1,451/100' Altitude: 71.2/10
    gpsDataFormated = {}
    gpsDataFormated['latitude'] = gpsData['latitude']
    gpsDataFormated['longitude'] = gpsData['longitude']
    gpsDataFormated['altitude'] = gpsData['altitude'] + '/10'
    return gpsDataFormated


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
    waypoint_a = {'latitude' : 41.56654, 'longitude': -74.0547, 'altitude' : 182}
    try:
        gpsp.start()
        while True:

            os.system('clear')
            gpsData = {'latitude' : gpsd.fix.latitude, 'longitude': gpsd.fix.longitude, 'altitude' : gpsd.fix.altitude}	# unformated gps data 	
            if(gpsData['latitude'] > 40.00):  #waypoint_a['latitude']):
                if(gpsData['longitude'] > -75.00): #waypoint_a['longitude']):
                    triggerCamera(gpsData)
                    print "Camera Triggered"
                            

    except (KeyboardInterrupt, SystemExit):
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join()
        print "Done. \nExiting."



# TODO gps reading
#gpsData = {
#triggerCamera(gpsData)
