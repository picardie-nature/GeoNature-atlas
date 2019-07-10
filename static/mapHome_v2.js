var map = generateMap();
var legend  = new L.Control(); ;

function getColor(d) {
    return d > 100  ? '#ad2272' :
           d > 80  ? '#9756b4' :
           d > 50  ? '#5a82e1' :
           d > 15  ? '#00a5f2' :
           d > 5  ? '#00c2e9' :
           '#00dad1';
}

function styleMailleAtlas(feature) {
    return {
        fillColor: getColor(feature.properties.n_obs),
        weight: 0.5,
        color: 'white',
        fillOpacity: 0.7
    };
}


legend.remove()
legend = L.control({position: 'topleft'});
legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    var grades = [1,5,15,50,80,100]
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i]) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(map);

$.getJSON( configuration.URL_APPLICATION+'/api/mailles/lastObs' ).done(function(data){
    console.log(data);

     currentLayer = L.geoJson(data, {
          onEachFeature : function (feature, layer){
                    prop=feature.properties;
                    popupContent = "<b>Nombre d'obs </b> "+prop.n_obs+"</b> ("+prop.n_taxons+ " taxons)";
                    layer.bindPopup(popupContent)
          },
          style: styleMailleAtlas,
      }).addTo(map);
})
