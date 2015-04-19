
// gallery images global
var CB_Gallery = []; // creates the array
CB_Gallery[0] = 'myphotos'; // name of the gallery

// global "map" variable
var map = null;
var bounds = null;
var infowindow = null;

var DataProcessing = (function () {
  var myDataProcessing = {};
  var imagesData = [];
  var markers = [];

  var _loadImagesData = function () {
    // $.getJSON('get-images.php', callback);
    $.ajax({
      url: 'get-images.php',
      dataType: 'json',
      async: false,
      success: function(data) {
        imagesData = data;
      }
    });
  };

  _loadImagesData();

  var _prepareGallery = function () {
  //prepare images array for gallery
    $.each(imagesData, function(index, element) {
        CB_Gallery[index + 1] = [];
        CB_Gallery[index + 1][0]= element["path_to_image"] ;
        CB_Gallery[index + 1][1]= "image" ;
        CB_Gallery[index + 1][2]= element["id"] ;
        CB_Gallery[index + 1][3]= 450 ;
        CB_Gallery[index + 1][4]= 338 ;
        CB_Gallery[index + 1][5]= element["path_to_image"] ;
        CB_Gallery[index + 1][9]= "on" ;
    });
  };

  _prepareGallery();

  // public methods

  myDataProcessing.getImages = function () {
    return imagesData;
  };

  myDataProcessing.getMarkers = function () {

    var data = imagesData;

    $.each(data, function (index, element) {

      //prepare markers for map
      markers[index] =  [ '<h3>Gallery</h3>',
        element.latitude,
        element.longitude,
        2,
        "<div class=\"infowindow\"><a href=" + element.path_to_image  + " onclick='jQuery.slimbox([[\"images/image-2.jpg\", \"caption 1\"], [\"images/image-1.jpg\", \"caption 2\"]], 0);return false' rel=\"lightbox-groupname\" ><img src=\"images/image-2-thumb.jpg\"><img src=\"images/image-1-thumb.jpg\"></a><br /><br /></div>"

        ];
    });

    return markers;
  };

  return myDataProcessing;

})();

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
      new google.maps.Point(0, 0),
      // The anchor for this image is the base of the flagpole at 0,32.
      new google.maps.Point(55, 55));
  var shadow = new google.maps.MarkerImage('images/drone-pi-icon.png',
      // The shadow image is larger in the horizontal dimension
      // while the position and offset are the same as for the main image.
      new google.maps.Size(55, 55),
      new google.maps.Point(0, 0),
      new google.maps.Point(0, 55));
      // Shapes define the clickable region of the icon.
      // The type defines an HTML &lt;area&gt; element 'poly' which
      // traces out a polygon as a series of X,Y points. The final
      // coordinate closes the poly by connecting to the first
      // coordinate.
  var shape = {
    coord: [1, 1, 1, 55, 55, 55, 55, 1],
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

function initialize() {

  var markers = DataProcessing.getMarkers();

  var myOptions = {
    zoom: 16,
    center: new google.maps.LatLng(41.744192, -74.083375),
    mapTypeId: google.maps.MapTypeId.HYBRID
  };
  var map = new google.maps.Map(document.getElementById("map_canvas"),
    myOptions);

  setMarkers(map, markers);
}

// replace the inline body onload event handler with a DOM listener
google.maps.event.addDomListener(window, 'load', initialize);
