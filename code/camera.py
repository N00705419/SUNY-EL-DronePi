import os
import datetime

class Camera(object):
    """Manages the camera for the raspberry pi"""

    def takePicture(self, cameraOptions, path_to_image):
    # receives a string with all the camera options available at
    # http://www.raspberrypi.org/documentation/raspbian/applications/camera.md
    # takes a picture and logs to the log.txt file

        takePictureCommand = 'raspistill --output ' + path_to_image + cameraOptions
        dateString = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        try:
            print "Sent picture command to camera"
            os.system(takePictureCommand)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            os.system( "echo 'ERROR: picture NOT saved' %s >> log.txt" % (dateString))
        else:
            os.system( "echo 'picture saved' %s >> log.txt" % (dateString))
            print "Picture saved successfuly."




