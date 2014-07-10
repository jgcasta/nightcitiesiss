/*

José Gómez Castaño

Departamento de Astrofísica y Ciencias de la Atmósfera
Facultad de CC Físicas
Universidad Complutense de Madrid
jgomez03@pdi.ucm.es

Georreferenciación de imágenes de satélite

Versión 10/07/2014

*/



var xy;
var lonlat;
var clickImg = false;
var clickMap = false;
var urlImage = '';

var firstTime = true;
var clickImg = false;
var clickMap = false;

var dimX,dimY;
var pixelProjection;


var iconStyle = new ol.style.Style({
  image: new ol.style.Circle({
      radius: 4,
      fill: new ol.style.Fill({
          color: [255, 204, 102, 1]
      }),
      stroke: new ol.style.Stroke({
          color: [255, 204, 102, 1],
          width: 1.5
      })
  }),
  zIndex: 1
});

var iconStyleVIIRS = new ol.style.Style({
  image: new ol.style.Circle({
      radius: 5,
      fill: new ol.style.Fill({
          color: [255, 0, 0, 1]
      }),
      stroke: new ol.style.Stroke({
          color: [255, 0, 0, 1],
          width: 1.5
      })
  }),
  zIndex: 1
});

var iconFeature;
var map;
var ISSlayer;

var mapOSM;
var osmlayer = new OpenLayers.Layer.OSM();
var gmaplayerSt = new OpenLayers.Layer.Google("Google Streets",{numZoomLevels: 20});
var gmaplayerSat = new OpenLayers.Layer.Google("Google Satellite",{type: google.maps.MapTypeId.SATELLITE, numZoomLevels: 22});

var fromProjection = new OpenLayers.Projection("EPSG:4326");   
var toProjection   = new OpenLayers.Projection("EPSG:900913");

var pointLayer;

var renderer = OpenLayers.Util.getParameters(window.location.href).renderer;
enderer = (renderer) ? [renderer] : OpenLayers.Layer.Vector.prototype.renderers;
var pointLayerOSM = new OpenLayers.Layer.Vector('Points', {
        styleMap: new OpenLayers.StyleMap({
            pointRadius: "5", 
            fillColor: "#fc0000"
        }),
        renderers: renderer
    });

var sourceViirs = new ol.source.WMTS({
    urls: [
        "https://map1a.vis.earthdata.nasa.gov/wmts-geo/wmts.cgi",
        "https://map1b.vis.earthdata.nasa.gov/wmts-geo/wmts.cgi",
        "https://map1c.vis.earthdata.nasa.gov/wmts-geo/wmts.cgi",
    ],
    layer: "VIIRS_CityLights_2012",
    format: "image/jpeg",
    matrixSet: "EPSG4326_500m",
    tileGrid: new ol.tilegrid.WMTS({
        origin: [-180, 90],
        resolutions: [
            0.5625,
            0.28125,
            0.140625,
            0.0703125,
            0.03515625,
            0.017578125,
            0.0087890625,
            0.00439453125,
            0.002197265625
        ],
        matrixIds: [0, 1, 2, 3, 4, 5, 6, 7, 8],
        tileSize: 512
    }),
    attributions: [
        new ol.Attribution({html:"NASA NPP - VIIRS"})
    ]
});

var viirs = new ol.layer.Tile({source: sourceViirs});


function loadUserProgress() {
    pybossa.userProgress('nightcitiesissfix').done(function(data){
        var pct = Math.round((data.done*100)/data.total);
        $("#progress").css("width", pct.toString() +"%");
        $("#progress").attr("title", pct.toString() + "% completed!");
        $("#progress").tooltip({'placement': 'left'}); 
        $("#total").text(data.total);
        $("#done").text(data.done);

    });
}


pybossa.taskLoaded(function(task, deferred) {
    if ( !$.isEmptyObject(task) ) {
        
        $("#success").hide();
        $("#loading").hide();

        task.answer = {
            'imageResult' : '',
            'XY': '',
            'LONLAT': '',
            'img_big': task.info.link_big,
            'dimX': '',
            'dimY': ''
        }

        deferred.resolve(task);
    }
    else {
        deferred.resolve(task);
    }
    updateTwitterValues(window.location.href);
});

pybossa.presentTask(function(task, deferred) {
    
    if ( !$.isEmptyObject(task) ) {
        
        loadUserProgress();

        // first time I load the whole map
        if (firstTime){
            loadOSM(task.info.citylon,task.info.citylat,9);
            loadISSImage(task.info.link_big);
            firstTime = false;
        }

        $("#question").html(task.info.question);
        $('#task-id').html(task.id);
        $('.btn-answer').off('click').on('click', function(evt) {
        $("#hrefPicture").attr("href",task.info.linkData);
        $("#fb-like").attr("data-href",task.info.linkData);


            var answer = $(evt.target).attr("value");
            urlImage = task.info.link_big;

            if (typeof answer != 'undefined') {

              if (answer == 'save'){

                
                $("#step1").hide();
                
                task.answer.XY = readAllValues(document.dataList.xyValues);
                task.answer.LONLAT = readAllValues(document.dataList.lonlatValues);
                xy = '';
                lonlat = '';
                task.answer.dimX = dimX;
                task.answer.dimY = dimY;
                
                pybossa.saveTask(task.id, task.answer).done(function() {
                    deferred.resolve();
                });
                console.log('datos salvados');

                $("#step1").show();
                $("#success").show();
                $("#loading").show();


                changeMapOSM(task.info.citylon,task.info.citylat,9);
                removeAllOptions();
                loadNewISSImage(urlImage);

              }else if (answer == '404'){
                removeAllOptions();
                
                changeMapOSM(task.info.citylon,task.info.citylat,9);
                loadNewISSImage(urlImage);   
                task.answer.imageResult = '404';
                pybossa.saveTask(task.id, task.answer).done(function() {
                    deferred.resolve();
                });  
                
              }else {
                removeAllOptions();
                
                changeMapOSM(task.info.citylon,task.info.citylat,9);
                loadNewISSImage(urlImage);   
                task.answer.imageResult = 'unknown';
                pybossa.saveTask(task.id, task.answer).done(function() {
                    deferred.resolve();
                });  
              }

            }
        });
        $("#loading").hide();
    }
    else {
        $(".skeleton").hide();
        $("#loading").hide();
        $("#finish").fadeIn(500);
    }
});

function updateTwitterValues(share_url) {
    $("#Twitter-share-section").html('&nbsp;'); 
    $("#Twitter-share-section").html('<a href="https://twitter.com/share" class="twitter-share-button" data-url="'+share_url+'" data-text="Check out this amazing image!" data-size="large" data-hashtags="citiesAtNight">Tweet</a>');
    twttr.widgets.load();
}

// functions to show ISS picture and OSM Map


function createISSLayer(urlImage, imgX, imgY){

     pixelProjection = new ol.proj.Projection({
      code: 'pixel',
      units: 'pixels',
      extent: [0, 0, eval(imgX), eval(imgY)] 

    });;

    ISSlayer = new ol.layer.Image({
        source: new ol.source.ImageStatic({
          attributions: [
            new ol.Attribution({
              html: '<a href="http://guaix.fis.ucm.es/DarkSkies">ISS - GUAIX UCM</a>'
            })
          ],
          url: urlImage,
          imageSize: [eval(imgX), eval(imgY)],
          projection: pixelProjection,
          imageExtent: pixelProjection.getExtent()
        })
      });
}



function loadISSImage(urlImage){

  var dim = new Array();
  var img = new Image();
  img.onload = function() {
      
      dim[0] = this.width;
      dim[1] = this.height;
      
      dimX = dim[0];
      dimY = dim[1];

      createISSLayer(urlImage, dimX, dimY); 
      
      map = new ol.Map({

        interactions: ol.interaction.defaults().extend([
          new ol.interaction.DragRotateAndZoom()
        ]),
        layers: [ISSlayer],

        target: 'map',

        view: new ol.View({
          projection: pixelProjection,
          center: ol.extent.getCenter(pixelProjection.getExtent()),
          zoom: 1
        })
      });

      map.on('click', function(evt) {
        var coordinate = evt.coordinate;
        var xy = ol.coordinate.toStringXY(ol.proj.transform(coordinate, pixelProjection, pixelProjection));

        if (clickImg == false){
          
          addOption(document.dataList.xyValues, xy,xy);

          addPointLayer();
          clickImg = true;
          clickMap = false;

        }
      });
  } // img.load
  img.src = urlImage;
  
} // loadISSImage

function unloadISSImage(){
  window.map.removeLayer(ISSlayer);
}

function loadNewISSImage(urlImage){

  var dim = new Array();
  var img = new Image();
  img.onload = function() {
    
    dim[0] = this.width;
    dim[1] = this.height;
    
    dimX = dim[0];
    dimY = dim[1];
  
    map.removeLayer(ISSlayer);
    createISSLayer(urlImage, dimX, dimY); 
    map.addLayer(ISSlayer);

  } // img.load
  img.src = urlImage;
}


function handleMapClick(evt) {

      if (clickMap == false){
        
        var lonlat = mapOSM.getLonLatFromViewPortPx(evt.xy).transform(new OpenLayers.Projection("EPSG:900913"), new OpenLayers.Projection("EPSG:4326"));
        var coord = lonlat.lon.toFixed(6) + ',' + lonlat.lat.toFixed(6);

        addOption(document.dataList.lonlatValues, coord,coord);
        
        addPointLayerOSM();
        clickMap = true;
        clickImg = false;
        mapOSM.addLayer(pointLayerOSM);  
      }
    } 


function loadOSM(lonOSM, latOSM, zoomOSM){

    mapOSM = new OpenLayers.Map({
        div: "mapOSM",
         projection: "EPSG:4326"
    });

    mapOSM.addLayers([gmaplayerSt,gmaplayerSat,osmlayer]);
    
    mapOSM.addControl(new OpenLayers.Control.LayerSwitcher());

    var centerPosition = new OpenLayers.LonLat(eval(lonOSM),eval(latOSM)).transform( fromProjection, toProjection);
    mapOSM.setCenter(centerPosition, zoomOSM );

    mapOSM.events.register('click', mapOSM, handleMapClick);


    //load VIIRS help map
    mapVIIRS = new ol.Map({
      target: 'mapVIIRS',
      layers: [
        viirs
      ],

      view: new ol.View({
        projection: ol.proj.get("EPSG:4326"),
                    extent: [-180, -90, 180, 90],
            center: [0, 0],
            zoom: 1
      })
    });

    var icons = [];
    nadirISS = new ol.Feature({ geometry: new ol.geom.Point([eval(lonOSM),eval(latOSM)])});
    nadirISS.setStyle(iconStyleVIIRS);
    icons.push(nadirISS); 

    nadirLayer = new ol.layer.Vector({ source: new ol.source.Vector({ features: icons }) });
  
    mapVIIRS.addLayer(nadirLayer);

}

function changeMapOSM(lonOSM, latOSM, zoomOSM){

  // change OSM
  var centerPosition = new OpenLayers.LonLat(eval(lonOSM),eval(latOSM)).transform( fromProjection, toProjection);
  mapOSM.setCenter(centerPosition, zoomOSM );

  // change VIIRS
  mapVIIRS.removeLayer(nadirLayer);
  var icons = [];
  nadirISS = new ol.Feature({ geometry: new ol.geom.Point([eval(lonOSM),eval(latOSM)])});
  nadirISS.setStyle(iconStyleVIIRS);
  icons.push(nadirISS); 

  nadirLayer = new ol.layer.Vector({ source: new ol.source.Vector({ features: icons }) });

  mapVIIRS.addLayer(nadirLayer);

}

function addPointLayer(){

  window.map.removeLayer(pointLayer);

  var pos = [];
  var icons = [];
  
  for(i=0;i<dataList.xyValues.options.length;i++){
    
    if(typeof dataList.xyValues.options[i].value != 'undefined'){
      
      pos = dataList.xyValues.options[i].value.split(',');

      iconFeature = new ol.Feature({ geometry: new ol.geom.Point([eval(pos[0]), eval(pos[1])])});
      iconFeature.setStyle(iconStyle);
      icons.push(iconFeature);    

    }
  }  

  pointLayer = new ol.layer.Vector({ 
    source: new ol.source.Vector({ features: icons }) 
  })
  
  map.addLayer(pointLayer);

}


function addPointLayerOSM(){
  
    var posOSM = [];
    var features = new Array(50);
  
    for(i=0;i<dataList.lonlatValues.options.length ;i++){

        if(typeof dataList.lonlatValues.options[i].value != 'undefined'){
          
            posOSM = dataList.lonlatValues.options[i].value.split(',');

            var point = new OpenLayers.Geometry.Point(eval(posOSM[0]), eval(posOSM[1]));
            point.transform(fromProjection, toProjection);
            var featureP = new OpenLayers.Feature.Vector(point);

            pointLayerOSM.addFeatures([featureP]);
        }
    }  

}

function removePoint(){

  window.map.removeLayer(pointLayer);

  if(typeof pointLayerOSM != 'undefined'){

    pointLayerOSM.destroyFeatures();

  }

}



// auxiliar functions

function addOption(selectbox,text,value ){
  var optn = document.createElement("OPTION");
  optn.text = text;
  optn.value = value;
  selectbox.options.add(optn);
}

var removed = false;
function removeOptions(){
    removed = true;
    pointLayerOSM.destroyFeatures();
    var xyDeleted = false;
    for(var i=0; i<dataList.xyValues.options.length-1;i++){
      
      if(dataList.xyValues.options[i].selected){
        window.map.removeLayer(pointLayer);
        dataList.xyValues.remove(i);
        dataList.lonlatValues.remove(i);
        xyDeleted = true;
        addPointLayer();
        addPointLayerOSM();
      }
      if( !xyDeleted && dataList.lonlatValues.options[i].selected ){
        window.map.removeLayer(pointLayer);
        dataList.lonlatValues.remove(i);
        dataList.xyValues.remove(i);
        xyDeleted = false;
        addPointLayerOSM();
        addPointLayer();
      }
    }
    
}

function removeAllOptions(){

    removePoint();

    document.getElementById('xyValues').options.length = 0;
    document.getElementById('lonlatValues').options.length = 0;

}

function readAllValues(selectbox){
  
  var i;
  var ret = new Array();
  for(i=0;i<selectbox.options.length;i++){
    
    if(typeof selectbox.options[i].value != 'undefined'){
      ret.push(selectbox.options[i].value + ';');
    }
  }  
  return ret;
}

function getIimDim(urlimage){
  var dim = new Array();
  var img = new Image();
  img.onload = function() {

    dim[0] = this.width;
    dim[1] = this.height;
  }
  img.src = urlimage;
  return dim;
}

pybossa.run('nightcitiesissfix');