<!DOCTYPE html>
<html>
<head>
  <title>Quick SLPK Server - viewer : {{slpk}}</title>
  <style>
    html,
    body,
    #viewDiv {
      padding: 0;
      margin: 0;
      height: 100%;
      width: 100%;
    }
  </style>

  <link rel="stylesheet" href="https://js.arcgis.com/4.6/esri/css/main.css">
  <script src="https://js.arcgis.com/4.6/"></script>

  <script>
    require([
      "esri/Map",
      "esri/views/SceneView",
      "esri/layers/SceneLayer",

      "dojo/domReady!"
    ], function(Map, SceneView, SceneLayer) {

      // Create Map
      var map = new Map({
        basemap: "dark-gray",
        ground: "world-elevation"
      });

      // Create the SceneView
      var view = new SceneView({
        container: "viewDiv",
        map: map,
      });

      // Create SceneLayer and add to the map
      var layer = new SceneLayer({
        url:"{{url}}",
        popupEnabled: true
      });
      map.add(layer);
	  
	  // Automatic zoom to layer extent
	layer.when(function(){
	  view.goTo(layer.fullExtent);
	});
	
	
    });
  </script>
</head>

<body>
  <div id="viewDiv"></div>
</body>
</html>
