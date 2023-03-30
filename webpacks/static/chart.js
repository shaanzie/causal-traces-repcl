function renderGraph(jsonResponse) {


    var namespace = joint.shapes;

    var graph = new joint.dia.Graph({}, { cellNamespace: namespace });

    var paper = new joint.dia.Paper({
        el: document.getElementById('myholder'),
        model: graph,
        width: '100%',
        height: '100%',
        gridSize: 1,
        cellViewNamespace: namespace
    });

    for(let process = 0; process < 64; process++) {

        var rect = new joint.shapes.standard.Rectangle();
        rect.position(100, 20 + 10*i);
        rect.attr({
            body: {
                fill: 'blue'
            },
            label: {
                text: 'Process ' + process,
                fill: 'white'
            }
        });
        rect.id = 'process' + process;
        rect.addTo(graph);

    }

    // var rect = new joint.shapes.standard.Rectangle();
    // rect.position(100, 30);
    // rect.resize(100, 40);
    // rect.attr({
    //     body: {
    //         fill: 'blue'
    //     },
    //     label: {
    //         text: 'Hello',
    //         fill: 'white'
    //     }
    // });
    // rect.addTo(graph);

    // var rect2 = rect.clone();
    // rect2.translate(300, 0);
    // rect2.attr('label/text', 'World!');
    // rect2.addTo(graph);

    // var link = new joint.shapes.standard.Link();
    // link.source(rect);
    // link.target(rect2);
    // link.addTo(graph);

}

function parseJSON() {

    const xhr = new XMLHttpRequest();

    xhr.open('GET', '/data', true);

    xhr.responseType = 'json';

    xhr.onload = function () {

        if (xhr.readyState == xhr.DONE && xhr.status == 200) {

            renderGraph(xhr.response);

        }

    };

    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhr.setRequestHeader('Access-Control-Allow-Headers', '*');
    xhr.setRequestHeader('Access-Control-Allow-Methods', '*');

    xhr.send();

}

setInterval(parseJSON, 5000);