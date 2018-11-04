
//test function
function test(){

  let train_data_url = `/api/data/train`;
  console.log(train_data_url);

  //read the data from json/api
  d3.json(train_data_url).then(data=> {
    console.log("train data:");
    console.log(data);

    //$("#pie_chart").html("");
  //var PIE = document.getElementById("pie_chart");
  //Plotly.newPlot(PIE, data, layout);
  });
};


function summaryTB(){

    let summary_url = `/api/data/train/summary`;
    //console.log(summary_url);
   
    var tbody = d3.select("#sumTbody");


    //read the data from json/api
    d3.json(summary_url).then(data=> {
      //console.log("train data summary:");
      //console.log(data);
      Object.entries(data).forEach(([key, value]) => {
          
          var row = tbody.append("tr");
          var cell = tbody.append("td");
          cell.text(value["stats"]);
          var cell = tbody.append("td");
          cell.text(value["item_outlet_sales"]);
          var cell = tbody.append("td");
          cell.text(value["outlet_years"]);
          var cell = tbody.append("td");
          cell.text(value["item_MRP"]);
          var cell = tbody.append("td");
          cell.text(value["item_weight"]);
          var cell = tbody.append("td");
          cell.text(value["item_visibility_mean_ratio"]);
      });
    });
  };


function corrTB(){

    let corr_url = `/api/data/train/corr`;
    //console.log(summary_url);
   
    var tbody = d3.select("#corrTbody");


    //read the data from json/api
    d3.json(corr_url).then(data=> {
      //console.log("correlation summary:");
      //console.log(data);
      Object.entries(data).forEach(([key, value]) => {
          
          var row = tbody.append("tr");
          var cell = tbody.append("td");
          cell.text(value["stats"]);
          var cell = tbody.append("td");
          cell.text(value["item_outlet_sales"]);
          var cell = tbody.append("td");
          cell.text(value["outlet_years"]);
          var cell = tbody.append("td");
          cell.text(value["item_MRP"]);
          var cell = tbody.append("td");
          cell.text(value["item_weight"]);
          var cell = tbody.append("td");
          cell.text(value["item_visibility_mean_ratio"]);
      });
    });
  };

function boxPlot(){
  let train_url = `/api/data/train`;
  var boxPlot = d3.select("#boxPlot");

  //read the data from json/api
  d3.json(train_url).then(data=> {
    let outlet_years = [];
    let outlet_size = [];
    let fat_content = [];
    let y_outlet_sale = [];

    Object.entries(data).forEach(([key, value]) => {
      outlet_years.push(value["outlet_years"]);
      outlet_size.push(value["outlet_size"]);
      fat_content.push(value["item_fat_content"]);
      y_outlet_sale.push(value["item_outlet_sales"]);

    });


});
};


function avgSalesBarChart() {

  var route = '/api/data/train/avg_item_sales';

  d3.json(route).then(function(data){
      // list to contain total sales of each outlet
      var avg_sale_per_item = [];
      var outlet_store = [];
      var total_items = [];

      data.forEach(function(data){
          data.avg_sale_per_item = +data.avg_sale_per_item;  
          data.total_sales = +data.total_sales;
          data.quantity_sold = +data.quantity_sold;
          
          //append total sales to list
          avg_sale_per_item.push(data.avg_sale_per_item);  
          //append outlet id to list
          outlet_store.push(data.outlet_id);
          //append total items sold to list
          total_items.push(`Total Items Sold: ${data.quantity_sold}`);
      });

      var trace = {
          x: outlet_store,
          y: avg_sale_per_item,
          type: 'bar',
          text: total_items,
          marker: {
              color: ['rgb(186,22,63)', 'rgb(121,37,117)','rgb(21,104,156)','rgb(38,156,98)','rgb(35,100,52)','rgb(56,161,152)','rgb(153,148,194)','rgb(211,102,151)','rgb(249,149,51)','rgb(244,206,109)']
          },
          aaxis: {
              showgrid: true,
              minorgridwidth: 1
          },
          mode: 'text',
          textposition: 'top'
      };

      var barChartData = [trace];
  
      var layout = {
          title: "Outlet's Average Sales per Item",
          titlefont: {
            size: 20
          }
      };
  
      Plotly.newPlot('barChart', barChartData, layout, {responsive: true});
  });
};


// doughnut chart function
function doughnutChart() {

  var route = '/api/data/train/avg_item_sales';

  d3.json(route).then(function(data){
      
      var total_sales_data = [];
      var outlet_store = [];

      data.forEach(function(data){
          
          data.total_sales = +data.total_sales;
          //append total sales to list
          total_sales_data.push(data.total_sales);          
          //append outlet id to list
          outlet_store.push(data.outlet_id);
      });      
      
      var ctx = document.getElementById("doughnut");

      var labelPercentage = total_sales_data;

      var doughnutChart = new Chart(ctx, {
          type: 'doughnut',
          data: {
              labels: outlet_store,
              datasets: [
                  {
                      data: total_sales_data,
                      label: 'Total Sales',
                      //label: labelPercentage.map( x => `${x/total}%`),
                      backgroundColor: ['rgb(186,22,63)', 'rgb(121,37,117)','rgb(21,104,156)','rgb(38,156,98)','rgb(35,100,52)','rgb(56,161,152)','rgb(153,148,194)','rgb(211,102,151)','rgb(249,149,51)','rgb(244,206,109)'],
                      borderColor: 'black'
                  }
              ]
          },
          options: {
              title: {
                  display: true,
                  position: 'top',
                  text: "Outlet's % of Company's Total Sales Revenue",
                  fontSize: 20,
                  fontStyle: 'bold'
              },
              cutoutPercentage: 30,
              animation: {
                  animateScale: true
              },
              tooltips: {
                  callbacks: {
                      label: function(tooltipItem, data) {
                          var pieData = data.datasets[tooltipItem.datasetIndex].data; 
                          var tooltipLabel = data.labels[tooltipItem.index];
                          var tooltipData = pieData[tooltipItem.index];

                          var total = 0;

                          for (var i = 0; i < total_sales_data.length; i++) {
                              total += total_sales_data[i];
                          }

                          var tooltipPercentage = parseFloat((tooltipData/total).toFixed(3)*100);
                          return tooltipLabel + ': ' + tooltipPercentage + '%';
                      }
                  }
              }
          }
      })
  });
  
};



function init() {

  test();
  summaryTB();
  corrTB();
  avgSalesBarChart();
  doughnutChart();
  boxPlots();
  heatmapplot();
};

// Initialize the app
init();

