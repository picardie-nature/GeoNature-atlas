var map = generateMap();
//generateSliderOnMap();
var legend = L.control({position: 'bottomright'});

// Legende

htmlLegend = "<i style='border: solid "+configuration.MAP.BORDERS_WEIGHT+"px "+configuration.MAP.BORDERS_COLOR+";'> &nbsp; &nbsp; &nbsp;</i> Limite du "+ configuration.STRUCTURE;
//generateLegende(htmlLegend);

legend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend');
    div.innerHTML += '<b>Dernière observation</b><br>';
    div.innerHTML +='<i style="background:green"></i> Moins de 5 ans<br>'
    div.innerHTML +='<i style="background:yellow"></i> 5 à 10 ans<br>'
    div.innerHTML +='<i style="background:red"></i> Plus de 10 ans<br>'
    return div;
};
legend.addTo(map);

// Current observation Layer: leaflet layer type
var currentLayer; 

// Current observation geoJson:  type object
var myGeoJson;

var compteurLegend = 0; // compteur pour ne pas rajouter la légende à chaque fois

function styleMailleAtlas(feature) {
    var fillColor ;
    var currentYear = new Date().getFullYear() ;
    var obsyear = feature.properties.lastyear ;
    if(feature.properties.lastyear <= currentYear - 10){
        fillColor='red' ;
    }else if(feature.properties.lastyear <= currentYear - 5) {
        fillColor='yellow';
    }else{
        fillColor='green';
    }

    return {
        fillColor: fillColor,
        weight: 0.5,
        color: 'white',
        fillOpacity: 0.8
    };
};

function shadowMaille(feature){
    s = styleMailleAtlas(feature);
    s.fillOpacity = 0.4;
    s.color = 'red';
    return s;
};


L.DomUtil.remove(sliderContainer); //Remove slider created in mapGenerator.js

$.ajax({
  url: configuration.URL_APPLICATION+'/api/observationsMailleLastObs/'+cd_ref, 
  dataType: "json",
  beforeSend: function(){
    $('#loadingGif').attr('src', configuration.URL_APPLICATION+'/static/images/loading.svg')
  }
  }).done(function(observations) {
    $('#loadingGif').hide();

  currentLayer = L.geoJson(observations, {
      onEachFeature : function (feature, layer){
                    popupContent = "<b>Nombre d'observations </b> "+feature.properties.nb_observations+"<br><b>Dernière d'observations </b>"+feature.properties.lastyear ;
                    layer.bindPopup(popupContent)
                    layer.on('mouseover',function(e){ layer.setStyle( shadowMaille(layer.feature) ); layer.bringToFront(); });
                    layer.on('mouseout ',function(e){ layer.setStyle( styleMailleAtlas(layer.feature) ); });
      },
      style: styleMailleAtlas,
  }).addTo(map);
  currentLayer.bringToFront();

});

