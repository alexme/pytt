    // .append("g")
    // .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

function parseData(dta_str) {
    var d = dta_str.trim().split('|');
    var id = Number(d[0]);
    var cat = d[1].split('.')[1];
    var num_data = d[2].replace(/[\[\] ]/g, "").trim().split(',').map(Number);
    return {'id': id, 'cat': cat, 'data': num_data};
}


function wsUpdate(event) {
    par_data = parseData(event.data);
    switch(par_data.cat) {
    case "PL":
        console.log("pl " + par_data.data);
        break;
    case "STREAM":
        console.log("data " + par_data.data);
        data_stack.push(par_data.data);
        redraw(data_stack, chart_data);
        break;
    case "POSITION":
        console.log("position " + par_data.data);
        break;
    default:
        console.log("got other cat");
}
}

function redraw(d, chart) {
    console.log('red')
    var circles = chart.selectAll('circle')
        .attr("class", "chart")
        .data(d);

    circles.enter().append('circle')
        .attr("cx", function(d) { return xScale(d[0]); })
        .attr("cy", function(d) { return yScale(d[1]); })
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
        .attr("cx", function(d) { return xScale(d[0]); })
        .attr("cy", function(d) { return yScale(d[1]); })
        .attr("r", function(d) { return 2; });
}

function startWs() {
    console.log("starting client");
    try {
        w = new WebSocket("ws://127.0.0.1:5678/");
    } catch (err) {
        console.log(err);
        return null;
    }
    w.onmessage = wsUpdate;
}