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

    gpsCoordinatesOptions = gpsData

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
  #Set to number of hardcoded coordinates
    hardCodedGPSCount = 1

  #when hardcoding the gps coordinates go to the 5th decimal for a range of 3.5ft from target or 
  #the 6th for a 0.36 ft from target
    waypoint_a = {'latitude' : 41.56654, 'longitude': -74.0547, 'altitude' : 182}
   
  #This could be one way to set the range. Just would have to do it for each longitude and latitude. Not sure if its legal with the subtraction 
  #within the range function
   w_aLatRange = range(waypoint_a['latitude'] - 0.00005, waypoint_a['latitude'] + 0.00005) 
   w_aLongRange = range(waypoint_a['longitude'] - 0.00005,waypoint_a['longitude'] +0.00005)
    try:
        gpsp.start()
        while True:

            os.system('clear')
            gpsData = {'latitude' : gpsd.fix.latitude, 'longitude': gpsd.fix.longitude, 'altitude' : gpsd.fix.altitude}	# unformated gps data 	
           
   #Compound if statement to test if in range of waypoint_a
             if gpsData['latitude'] in w_aLatRange and (gpsData['longitude'] in waypoint_a['longitude'] and  gpsData['altitude'] >= waypoint_a['altitude'] : 
                    triggerCamera(gpsData)
                    print "Camera Triggered"
                    hardCodedGPSCount -= 1
	#once we take the picture we want it to sleep until we get out of the waypoint range
		    sleep(10)
            if hardCodedGPSCount == 0:              
	 	print "\nMission Complete!!"   
		print "\nKilling Thread..."
		gpsp.join()   
	 	break
    except (KeyboardInterrupt, SystemExit):
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join()
        print "Done. \nExiting."



# TODO gps reading
#gpsData = {
#triggerCamera(gpsData)
