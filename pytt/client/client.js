var margin = { top: 20, right: 20, bottom: 30, left: 40 };
var width = 600 - margin.left - margin.right;
var height = 400 - margin.top - margin.bottom;
var data = new Array();

var xScale = d3.scaleLinear()
    .domain([90, 110])  // domaine d'entrée
    .range([0, width]);  // domaine de sortie


var yScale = d3.scaleLinear()
    .range([90, 110])
    .domain([height, 0]);


function colScale(i) {
    return d3.schemeCategory20(i % 20);
}

var chart = d3.select('#chart').append('svg')
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

function parseData(dta_str) {
    return "";
}


function wsUpdate(event) {
    numData = parseData(event.data);
    console.log(event.data)
};

function startWs() {
    console.log("starting client");
    var ws = new WebSocket("ws://127.0.0.1:5678/");
    ws.onmessage = wsUpdate;
}