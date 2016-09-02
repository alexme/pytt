var margin = { top: 20, right: 20, bottom: 30, left: 40 };
var width = 800 - margin.left - margin.right;
var height = 600 - margin.top - margin.bottom;
var data = new Array();

var xScale = d3.scaleLinear()
    .domain([90, 110])  // domaine d'entrée
    .range([0, width]);  // domaine de sortie


var yScale = d3.scaleLinear()
    .range([90, 110])
    .domain([height, 0]);

var chart = d3.select("body").select("div#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);

console.log(chart);