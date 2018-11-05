function mlBarPlots() {

  var data_url = `/api/data/models/summary`;
      
  d3.json(data_url).then(function(data){
    var model_type = [];
    var RMSE_value = [];

    data.forEach(function(data){
      data.model = data.model;
      data.RMSE = +data.RMSE;

      model_type.push(data.model);
      RMSE_value.push(data.RMSE)
    });

  var trace = {
    x: model_type, 
    y: RMSE_value,
    type: 'bar',
    textposition: 'auto',
    hoverinfo: RMSE_value,
    marker: {
      color: 'rgb(158,202,225)',
      opacity: 0.6,
      line: {
        color: 'rbg(8,48,107)',
        width: 1.5
      }
    }
  };

  var data = [trace];

  var layout = {
    
    yaxis: {title: "RMSE", range: [1080, 1100]},
    bargap: 0.05,
    };

  Plotly.newPlot('ml_bar', data, layout);

  })
  
  };

//  function init() {
//    barPlots();
//  };
  
  // Initialize the app
//  init();
      
          
