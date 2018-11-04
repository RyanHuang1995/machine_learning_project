
function boxPlots() {


let train_data_url = `/api/data/train`;

a = [1,2,3];
console.log(typeof a)
    
d3.json(train_data_url).then(data => {
        
        array=[];
    
        for (var index = 0; index < data.length; index ++) {
            array.push(data[index]);
    
        };
        
    console.log(array.length);
        
    
document.getElementById("myBtn").addEventListener("click", boxPlots);
    

var selection1 = document.getElementById("selection1");
var s1 = selection1.options[selection1.selectedIndex].value;

var selection2 = document.getElementById("selection2");
var s2 = selection2.options[selection2.selectedIndex].value;

console.log(s1);
console.log(s2);

var full = array.length;

items = [];
var j;
for (j = 0; j < full; j++){
items.push(array[j][s1])
};

var selection = Array.from(new Set(items))

console.log(selection);

var i;
var len = selection.length;
console.log(len);

data = [];

for (i = 0; i < len; i ++){


    var filterArray = selection[i];

    var filtered = array.filter(function(item) {
    return filterArray.indexOf(item[s1]) !== -1;
    });


    var x = [];
    var y = [];


    var num = Object.keys(filtered).length;


    var step;
    for (step = 0; step < num; step ++){
        x.push(filtered[step][s2])
        y.push(filtered[step]["item_outlet_sales"]);
    };

   
    var trace = {
        y: y,
        x: x,
        name: filterArray,
        type: "box"
    }; 


    data.push(trace);
 

};


console.log(data);



var layout = {
  yaxis: {
    title: 'Item Outlet Sales',
    zeroline: false
  },
  boxmode: 'group'
};



Plotly.newPlot('myDiv', data, layout);


});
};