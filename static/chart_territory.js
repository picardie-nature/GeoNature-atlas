var drawChart = function(elementId, labels, data, title){ 
    var ctx = document.getElementById(elementId).getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'doughnut',

        // The data for our dataset
        data: {
            labels: labels,
            datasets: [{
                label: 'Nombre d\'espèces',
                backgroundColor: ["#4cd195", "#f1f58c","#92baed","#adf7b8","#f18e8e","#ffbb00","#cc0066","#cccc00"],
                borderColor: 'rgb(255, 255, 255)',
                data: data
            }]
        },

        // Configuration options go here
        options: {
            legend:{ display : false },
            title:{
                display: (typeof title  !== "undefined") ? true : false,
                text: title
            }
        }
    });

}

var drawChartTerritorieKnoweldgeEvolution = function(elementId, labels, dataTaxon,dataOccurence , title){ 
    var ctx = document.getElementById(elementId).getContext('2d');
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data:{
            labels:labels,
            datasets: [
                {
                    label:"Observations",
                    fill:false,
                    borderColor:'rgba(255,102,0,0.8)',
                    backgroundColor:'rgba(0,102,255,0)',
                    data:dataOccurence,
                    yAxisID:'right-axis'
                },
                {
                    label:'Espèces',
                    data:dataTaxon,
                    borderColor:'rgba(0,128,0,1)',
                    backgroundColor:'rgba(0,128,0,0.3)',
                    yAxisID:'left-axis'
                }
            ]
        },
        options: {
            legend:{ display : true },
            title:{
                display: (typeof title  !== "undefined") ? true : false,
                text: title
            },
            scales:{
                yAxes: [{
                    id: 'left-axis',
                    type: 'linear',
                    position:'left'
                }, {
                    id: 'right-axis',
                    type: 'linear',
                    position:'right'
                }]
            },
            tooltips: {
                mode:'index'
            }
        }
    });


};

