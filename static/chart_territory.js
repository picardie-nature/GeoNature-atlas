var drawChart = function(elementId, labels, data){ 

    var ctx = document.getElementById(elementId).getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'doughnut',

        // The data for our dataset
        data: {
            labels: labels,
            datasets: [{
                label: 'Nombre d\'espèces',
                backgroundColor: ["#4cd195", "#f1f58c","#92baed","#adf7b8","#f18e8e"],
                borderColor: 'rgb(255, 255, 255)',
                data: data
            }]
        },

        // Configuration options go here
        options: {
            legend:{ display : false }
        }
    });


}

