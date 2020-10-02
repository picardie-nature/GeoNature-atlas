function makeCalHeatmap(itemSelector,cd_nom){
                    var cal = new CalHeatMap();
                    now= new Date()
                    var data_parser = function(raw_data){
                    	var stats = {};
                        for (var d in raw_data){
                            var t = new Date(raw_data[d].timestamp);
                            
                            var t = new Date(now.getFullYear(),0,1);
                            var t2 = t.getTime()/1000 + raw_data[d].doy*24*60*60
                            stats[t2] = raw_data[d].nb_obs;
                        }
                        console.log(stats);
                        return stats;

                    }

                    moment.locale("fr"); 
                    cal.init({
                            start: new Date(2020, 0),
                            range:12,
                        	itemSelector:itemSelector,
                        	domain: "month",
	                        subDomain: "day",
                            data: "https://geonature.clicnat.fr/api/myapi/calendar_heatmap/?cd_nom="+cd_nom,
                            afterLoadData: data_parser,
                           /* legend:[2, 10, 50, 100,150],
                            legendOrientation: "vertical",legendHorizontalPosition: "right",
                            legendVerticalPosition: "center",*/
                            itemName: ["observation", "observations"],
	                        subDomainTitleFormat: {
		                        empty: "Aucune données pour le {date}",
		                        filled: "{count} {name} le {date}"
	                        },
	                        legendTitleFormat: {
		                        lower: "Moins de {min} {name}",
		                        inner: "Entre {down} et {up} {name}",
		                        upper: "Plus de {max} {name}"
	                        },
	                        //domainLabelFormat: "%b %y",
                            domainLabelFormat : function(date) {
		                        return moment(date).format("MMM"); // Use moment.js library to translate date
	                        },
	                        subDomainDateFormat:  function(date) {
		                        return moment(date).format("Do MMM"); // Use moment.js library to translate date
	                        },
                            cellSize:10,cellPadding:2,rowLimit:10,
                            highlight: new Date()
                    });
}
