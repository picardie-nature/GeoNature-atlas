data = [
    {
        name:'Oiseaux',
        y: 94
        
    },
    {
        name:'Mammifères',
        y: 12  
    },
    {
        name:'Libellules',
        y: 25
    }
];



// Create the chart
Highcharts.chart('pie_chart', {
    chart: {
        type: 'pie'
    },
    title: {
        text: null
    },
    subtitle: {
        text: null
    },
    plotOptions: {
        pie: {
            shadow: false,
            center: ['50%', '50%']
        }
    },
    tooltip: {
        valueSuffix: ''
    },
    series: [{
        data:data,
        name:'Espèces'


    }]        

});
