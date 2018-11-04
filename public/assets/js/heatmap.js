
// build heatmap

function heatmapplot() {

    let corr_data_url = `/api/data/train/corr`;
    console.log(corr_data_url);

    //read the data from json/api
    d3.json(corr_data_url).then(function(data) {
        // console.log("train data:");
        var x_value=[];
        var y_value=[];
        // var z_value=[[1.0,0.5675,-0.0036,0.026,-0.0050199],[0.5675,1.0,-0.3911,0.01326,0.04913],[0.026,0.01326,0.00764,1.0,0.0128],[-0.005019,0.049,0.268,0.012822,1],[-0.003626,-0.3911151,1.0,0.00764,0.268]];
        var z_value=[];
        console.log(data);
        
        data.forEach(function(data){

            x_value.push(data.stats);
            y_value.push(data.stats);
           
            z_list=[];
            z_list.push(data.item_MRP.toFixed(2));
            z_list.push(data.item_outlet_sales.toFixed(2));
            z_list.push(data.item_weight.toFixed(2));
            z_list.push(data.outlet_years.toFixed(2));
            z_list.push(data.item_visibility_mean_ratio.toFixed(2));
            
            z_value.push(z_list);          

        });


       console.log(x_value);
       console.log(y_value);
       console.log(z_value);
        
        var data=[{
            type: 'heatmap',
            x:x_value,
            y:y_value,
            z:z_value
        }];
        var layout={
            //height: 600,
            //width: auto,
            //title:"Correlation Heapmap",
            annotations: [],
            xaxis:{
                type:"Item MRP"
            },
            
            yaxis: {
                autorange: true,
                //automargin: true,
                tickangle: 65,
                        },
           
            //margin:{
            //    l:200
             //       },
      
            
        };


        for ( var i = 0; i < y_value.length; i++ ) {
            for ( var j = 0; j < x_value.length; j++ ) {
              var currentValue = z_value[i][j];
              if (currentValue != 0.0) {
                var textColor = 'white';
              }else{
                var textColor = 'black';
              }
              var result = {
                xref: 'x1',
                yref: 'y1',
                x: x_value[j],
                y: y_value[i],
                text: z_value[i][j],
                font: {
                  family: 'Arial',
                  size: 12,
                  color: 'rgb(50, 171, 96)'
                },
                showarrow: false,
                font: {
                  color: textColor
                }
              };
              layout.annotations.push(result);
            }
          };

        Plotly.newPlot('myDiv2', data,layout);

    });
};


//function init() {

//    heatmapplot();

//};

// Initialize the app
//init();
