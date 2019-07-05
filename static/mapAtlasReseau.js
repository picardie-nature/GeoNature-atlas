var map = generateMap();


var currentLayer; 
var currentIdListe;
var legend  = new L.Control(); ;

var myGeoJson;


function styleMailleAtlas(feature) {
    var fillColor = 'yellow';
    if(feature.properties.n_sp > 10){ fillColor='green' }
    return {
        fillColor: getColor(feature.properties.n_sp),
        weight: 0.5,
        color: 'white',
        fillOpacity: 0.95
    };
}

/******* LEGEND **********/
function getColor(d) {
    grades = getGrades(currentIdListe);
    return d > grades[4]  ? '#E31A1C' :
           d > grades[3]  ? '#FC4E2A' :
           d > grades[2]  ? '#FD8D3C' :
           d > grades[1]  ? '#FEB24C' :
           d > grades[0]  ? '#FED976' :
           '#FFEDA0';
}

function getGrades(id_liste){
    return id_liste == 3 ? [1,5,10,15] : //micro mamm
           id_liste == 4 ? [1,5,10,15] : //chiro
           id_liste == 6 ? [1,5,20,35] : //odonates
           id_liste == 55 ? [1,5,10,15] : //grand mammifères terrestres
           id_liste == 50 ? [1,5,20,35] : //mammifères
           [1,2,3,4,5]; 

}

function setLegend(grades)
{
    legend.remove()
    legend = L.control({position: 'topleft'});
    legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),
            labels = [];

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML +=
                '<i style="background:' + getColor(grades[i] + 1,grades) + '"></i> ' +
                grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
        }

        return div;
    };

    legend.addTo(map);
}

/**********/


function changeLayer(id_reseau){
    //console.log(id_reseau);
    currentIdListe = id_reseau;
    setLegend(getGrades(id_reseau));
    if (map.hasLayer(currentLayer)) {currentLayer.remove()};
    $.ajax({
          url: configuration.URL_APPLICATION+'/api/atlasReseau/'+id_reseau, 
          dataType: "json",
          beforeSend: function(){
            $('#loadingGif').attr('src', configuration.URL_APPLICATION+'/static/images/loading.svg');
          }
          }).done(function(observations) {
            //$('#loadingGif').hide();
          currentLayer = L.geoJson(observations, {
              onEachFeature : function (feature, layer){
                        popupContent = "<b>Nombre d'espèces </b> "+feature.properties.n_sp+"</b>";
                        layer.bindPopup(popupContent)
              },
              style: styleMailleAtlas,
          }).addTo(map);
            currentLayer.bringToFront();

            currentLayer.on('popupopen',function(e){
                //console.log(e);
                feature = e.layer.feature;
                id_maille = feature.properties.id_maille;
                id_reseau = currentIdListe;

                $.ajax({
                  url: configuration.URL_APPLICATION+'/api/atlasReseau/mailles/'+id_maille+'/'+id_reseau, 
                  dataType: "json"})
                  .done(function(data){
                        var n_col = (data.features.length >= 6) ? 2 : 1;
                        if(e.popup.getContent().includes('<ul')){ return }; //si la popup est déjà ouverte
                        var str_list_sp='<ul style="columns:'+n_col+';">';
                        data.features.forEach(function(item,index){
                            str_list_sp+='<li style="list-style-type:square"><i>'
                            str_list_sp+='<a data-toggle="tooltip" href=/atlas/espece/'+item.properties.cd_nom+' ';
                            str_list_sp+='title="'+item.properties.nom_vern+'">'
                            str_list_sp+=item.properties.lb_nom
                            str_list_sp+='</a></i></li>';
                        });
                        tr_list_sp=str_list_sp+'</ul>';
                        //console.log(str_list_sp)
                        e.popup.setContent(e.popup.getContent()+str_list_sp);
                  });
            });           
     });
};



function getSpeciesInMaille(id_maille,id_reseau){
    $.ajax({
          url: configuration.URL_APPLICATION+'/api/atlasReseau/mailles/'+id_maille+'/'+id_reseau, 
          dataType: "json"})
          .done(function(data){
                $( "#liste_sp" ).html('blablabla');
            });

}

changeLayer(3);
