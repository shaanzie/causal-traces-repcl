function drawProcesses() {

    var numProcesses = 5;

    var maxX = 300;

    var layout = {

        title: 'Graph View',
        xaxis: {
            title: 'HLC',
            range: [-20, maxX],
            showgrid: false,
            zeroline: false
        },
        yaxis: {
            title: 'Processes',
            range: [0, numProcesses * 100 + 100],
            showgrid: false,
            showticklabels: false,
            zeroline: false
        },
        shapes: [],
        annotations: []
    }

    for (var i = 0; i < numProcesses; i++) {

        layout.shapes.push({
            type: 'rect',
            xref: 'x',
            yref: 'y',
            x0: -20,
            x1: 0,
            y0: 100 * i + 100,
            y1: 100 * i + 150,
            fillcolor: 'rgba(0, 100, 250, 0.2)',
            line: {
                width: 0
            }
        });

        layout.annotations.push({
            x: -20,
            y: (100 * i + 100 + 100 * i + 150) / 2, // Center of the box
            text: 'P' + i,
            showarrow: false,
            xanchor: 'left',
            yanchor: 'middle',
            font: {
                color: 'black',
                size: 12
            }
        });

        var centerY = (100 * i + 100 + 100 * i + 150) / 2;

        layout.shapes.push({
            type: 'line',
            xref: 'x',
            yref: 'y',
            x0: 0,
            x1: maxX, // Adjust this based on your x-axis end point
            y0: centerY,
            y1: centerY,
            line: {
                color: 'black',
                width: 0.5
            }
        });


    }

    Plotly.newPlot('graph', [], layout);

    var bubbleTrace = []
    for (var j = 0; j < trace['trace'].length; j++) {
        var event = trace['trace'][j];
        var pid = j % 5;

        var bubbleX = event['event_time']['hlc'];
        var bubbleY = (100 * pid + 100 + 100 * pid + 150) / 2;

        var bubbles = {
            x: [bubbleX],
            y: [bubbleY],
            mode: 'markers',
            marker: {
                size: 5,
                color: 'rgba(255, 0, 0, 0.7)', // Red color with opacity
                line: {
                    color: 'rgba(0, 0, 0, 1)', // Black border
                    width: 2
                }
            },
            type: 'scatter'
        };

        bubbleTrace.push(bubbles);
    }

    console.log(bubbleTrace);

    for (var i = 0; i < bubbleTrace.length; i++) {
        Plotly.plot('graph', [bubbleTrace[i]], layout);
    }

}