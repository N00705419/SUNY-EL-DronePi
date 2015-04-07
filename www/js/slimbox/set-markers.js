

// global "map" variable
      var map = null;
      var bounds = null;
      var infowindow = null;


// create the markers 

var markers = [
  ['<h3>Slimbox: Image Slideshow Old Main</h3>', 41.744192, -74.083375, 2, "<div class=\"infowindow\"><p>This example produces a lightbox for an image array, over Old Main.</p><a href=\"images/image-1.jpg\" onclick='jQuery.slimbox([[\"images/image-2.jpg\", \"caption 1\"], [\"images/image-1.jpg\", \"caption 2\"]], 0);return false' rel=\"lightbox-groupname\" ><img src=\"images/image-2-thumb.jpg\"><img src=\"images/image-1-thumb.jpg\"></a><br /><br /></div>"]];



function initialize() {
  var myOptions = {
    zoom: 16,
    center: new google.maps.LatLng(41.744192, -74.083375),
    mapTypeId: google.maps.MapTypeId.HYBRID
  }
  var map = new google.maps.Map(document.getElementById("map_canvas"),
                                myOptions);

  setMarkers(map, markers);
}

function setMarkers(map, locations) {
  // Add markers to the map

  // Marker sizes are expressed as a Size of X,Y
  // where the origin of the image (0,0) is located
  // in the top left of the image.

  // Origins, anchor positions and coordinates of the marker
  // increase in the X direction to the right and in
  // the Y direction down.
  var image = new google.maps.MarkerImage('images/drone-pi-icon.png',
      // This marker is 24 pixels wide by 26 pixels tall.
      new google.maps.Size(55, 55),
      // The origin for this image is 0,0.
      new google.maps.Point(0,0),
      // The anchor for this image is the base of the flagpole at 0,32.
      new google.maps.Point(55, 55));
  var shadow = new google.maps.MarkerImage('images/drone-pi-icon.png',
      // The shadow image is larger in the horizontal dimension
      // while the position and offset are the same as for the main image.
      new google.maps.Size(55, 55),
      new google.maps.Point(0,0),
      new google.maps.Point(0, 55));
      // Shapes define the clickable region of the icon.
      // The type defines an HTML &lt;area&gt; element 'poly' which
      // traces out a polygon as a series of X,Y points. The final
      // coordinate closes the poly by connecting to the first
      // coordinate.
  var shape = {
      coord: [1, 1, 1, 55, 55, 55, 55 , 1],
      type: 'poly'
  };
  for (var i = 0; i < locations.length; i++) {
    var mymarker = locations[i];
    var myLatLng = new google.maps.LatLng(mymarker[1], mymarker[2]);
    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        shadow: shadow,
        icon: image,
        shape: shape,
        title: mymarker[0],
		html:  "<p>" + mymarker[0] + "</p>" + mymarker[4], 
        zIndex: mymarker[3]
    });
	

	// create a content "shell" for the infowindow
	var contentString = "Some content";

            var infowindow = new google.maps.InfoWindow({
                content: contentString
            });

		
            google.maps.event.addListener(marker, "click", function () {
       

		// close any open infowindows	     
        infowindow.close();
     
               infowindow.setContent(this.html);
                infowindow.open(map, this);
                infowindow.zIndex(10);
            });			
  }
}

// replace the inline body onload event handler with a DOM listener
      google.maps.event.addDomListener(window, 'load', initialize);
