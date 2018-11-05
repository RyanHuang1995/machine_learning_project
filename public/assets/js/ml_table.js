function mlTB(){

    //"/api/data/models/dec_tree/prediction"
    let prediction_url = `/api/data/models/dec_tree/prediction`;
    //console.log(summary_url);
   
    var tbody = d3.select("#predictionTB");


    //read the data from json/api
    d3.json(prediction_url).then(data=> {
      //console.log("train data summary:");
      //console.log(data);
      Object.entries(data).forEach(([key, value]) => {
          
          var row = tbody.append("tr");
          var cell = tbody.append("td");
          cell.text(value["item_MRP"]);
          var cell = tbody.append("td");
          cell.text(value["item_fat_content"]);
          var cell = tbody.append("td");
          cell.text(value["item_sales"]);
          var cell = tbody.append("td");
          cell.text(value["item_type"]);
          var cell = tbody.append("td");
          cell.text(value["item_visibility_mean_ratio"]);
          var cell = tbody.append("td");
          cell.text(value["outlet_location_type"]);
          var cell = tbody.append("td");
          cell.text(value["outlet_size"]);
          var cell = tbody.append("td");
          cell.text(value["outlet_type"]);
          var cell = tbody.append("td");
          cell.text(value["outlet_years"]);
      });
    });

    //$(document).ready(function () {
    //    $('#prediction-table').DataTable();
    //});
    $(document).ready(function() { 
      $('#prediction-table') 
      .tablesorter({widthFixed: true, widgets: ['zebra']}) 
      .tablesorterPager({container: $("#pager")}); 
  }); 

  };