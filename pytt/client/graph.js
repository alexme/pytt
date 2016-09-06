var margin = { top: 20, right: 20, bottom: 30, left: 40 };
var width = 300 - margin.left - margin.right;
var height = 200 - margin.top - margin.bottom;

// data stacks
var data_stack = new Array();
var pl_stack = new Array();
var position_stack = new Array();

var xScale = d3.scaleLinear()
    .domain([90, 110])  // domaine d'entrée
    .range([0, width]);  // domaine de sortie


var yScale = d3.scaleLinear()
    .range([100, 120])
    .domain([height, 0]);

function colScale(i) {
    return d3.schemeCategory20[i % 20];
}

var charts = d3.select("body").selectAll("div.chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);

var chart_data = d3.select("body").select("div#data").select("svg");
var chart_pl = d3.select("body").select("div#pl").select("svg");
var chart_position = d3.select("body").select("div#position").select("svg");
