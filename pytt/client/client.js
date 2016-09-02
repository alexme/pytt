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

var chart = d3.select('#chart').append('svg')
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);
    // .append("g")
    // .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


function colScale(i) {
    return d3.schemeCategory20(i % 20);
}

function parseData(dta_str) {
    var data = dta_str.replace(/[\[\] ]/g, "").trim().split(',').map(Number);
    return data;
}


function wsUpdate(event) {
    numData = parseData(event.data);
    console.log("new -> " + numData);
    data.push(numData);
    redraw(data);
}

function redraw(d) {
    console.log('red')
    var circles = chart.selectAll('circle')
        .attr("class", "chart")
        .data(d);

    circles.enter().append('circle')
        .attr("cx", function(d) { return xScale(d.x); })
        .attr("cy", function(d) { return yScale(d.y); })
        .attr("r", 1);

    // circles.exit()
    //     .transition()
    //     .duration(750)
    //     .attr("r", 0)
    //     .remove();

    // Voici maintenant le traitement effectués sur les nœuds liés à
    // des données existantes. Notez que les nœuds de la sélection `enter`
    // seront également concernés ici.
    circles
        .attr("fill", function(d, i) { return colScale(i); })
        .transition()
        .duration(750)
        .attr("cx", function(d) { return xScale(d.x); })
        .attr("cy", function(d) { return yScale(d.y); })
        .attr("r", function(d) { return 2; });
}

function startWs() {
    console.log("starting client");
    var delay = 1;
    var ws = null;
    function f() {
        try {
            w = new WebSocket("ws://127.0.0.1:5678/");
        } catch (err) {
            console.log(err);
            return null;
        }
        return w;
    }
    ws = f();
    if (ws != null) {
        ws.onmessage = wsUpdate;
    }
}