function renderGraph(jsonResponse) {

    const container = document.getElementById("paper");
    const { graph, paper } = make_blank_chart(container);

    // Making process boxes
    make_process_boxes(graph);

    jsonResponse.forEach(function (event) {
        make_link(event, paper);
    });

    paper.on('cell:pointerdown', function (cellView) {
        var link = cellView.model.id.split(',')
        var proc_send = link[0];
        var send_time = link[2];
        console.log(link);
        make_proc_chart(jsonResponse, proc_send, send_time);
    });

}

function make_blank_chart(container) {

    var namespace = joint.shapes;

    var graph = new joint.dia.Graph({}, { cellNamespace: namespace });

    const paperWidth = '100%';
    const paperHeight = '100%';


    var paper = new joint.dia.Paper({
        el: container,
        model: graph,
        width: paperWidth,
        height: paperHeight,
        gridSize: 1,
        cellViewNamespace: namespace,
        padding: 0,
        fitToContent: false,
        autoResize: true
    });

    return { graph, paper }

}


function make_process_boxes(graph) {

    for (let process = 0; process < 10; process++) {

        var rect = new joint.shapes.standard.Rectangle();
        rect.position(100, 30 + 100 * process);
        rect.resize(50, 50);
        rect.attr({
            body: {
                fill: 'blue'
            },
            label: {
                text: 'P' + process,
                fill: 'white'
            }
        });
        rect.addTo(graph);

        const pageWidth = new joint.g.Point({ x: document.documentElement.clientWidth, y: 0 }).x;
        const midX = rect.getBBox().center().x;
        const endPoint = { x: pageWidth, y: rect.getBBox().center().y };

        const horizontalLine = new joint.dia.Link({
            source: { id: rect.id },
            target: { x: endPoint.x, y: endPoint.y },
            vertices: [
                { x: midX + 25, y: rect.getBBox().center().y },
                { x: endPoint.x + 25, y: rect.getBBox().center().y }
            ]
        });

        graph.addCell(horizontalLine);

    }
}

function make_link(event, paper) {
    var process_send = event.e;
    var process_recv = event.f;
    var failure = event.failure;
    var msg = event.msg;
    var send_clock = event['e.clock'];
    var recv_clock = event['f.clock'];
    var send_time = send_clock[process_send];
    var recv_time = recv_clock[process_recv];



    if (failure) {
        color = 'red'
    }
    else {
        color = 'white'
    }

    if (process_send != process_recv) {
        var link = new joint.dia.Link({
            id: process_send + ',' + process_recv + ',' + send_time + ',' + recv_time,
            source: { x: 225 * (send_time + 1), y: 55 + (100 * process_send) },
            target: { x: 225 * (recv_time + 1), y: 55 + (100 * process_recv) },
            attrs: {
                '.connection': { stroke: 'black', 'stroke-width': 2 },
                '.marker-target': { d: 'M 10 0 L 0 5 L 10 10 z' },
                '.marker-target-overflow': { 'x': 0, 'y': 0 },
                line: {
                    name: process_send + ',' + process_recv + ',' + send_time + ',' + recv_time
                }
            },
            labels: [
                {
                    position: 0.5, // Position the label at the midpoint of the link
                    attrs: {
                        text: {
                            text: msg + "\n" + send_clock, // The text to display
                            fill: 'black', // The color of the text
                            'font-size': 14, // The font size of the text
                            'font-weight': 'bold', // The font weight of the text
                            'text-anchor': 'middle', // Center the text horizontally
                            'y-alignment': 'middle', // Center the text vertically
                        },
                        rect: {
                            fill: color, // The background color of the label
                            rx: 5, // The corner radius of the label
                            ry: 5,
                            stroke: 'black', // The border color of the label
                            'stroke-width': 1, // The border width of the label
                        }
                    }
                }
            ]
        });
        paper.model.addCell(link);
    }
}

function make_proc_chart(jsonResponse, proc_send, proc_time) {

    const myDiv = document.getElementById('process-container');
    myDiv.style.display = 'block';
    const container = document.getElementById("procpaper");
    process_log = document.getElementById('processLog');
    const { graph, paper } = make_blank_chart(container);

    // Making process boxes
    make_process_boxes(graph);

    jsonResponse.forEach(function (event) {

        var failure = event.failure;
        var msg = event.msg;
        var send_clock = event['e.clock'];
        var recv_clock = event['f.clock'];    
        var send_time = send_clock[proc_send];
        var recv_time = recv_clock[proc_send];

        if ((event.e == proc_send || event.f == proc_send) && (send_time <= proc_time || recv_time <= proc_time)) {
            make_link(event, paper);
            process_log.innerHTML += "Event logged: process " + event.e + " (" + send_clock + ")" + ' to process ' + event.f + " (" + recv_clock + ")" + " : " + msg;
            if (failure) {
                process_log.innerHTML += " (FAILURE) "
            }
            process_log.innerHTML += "<br>";

        }

    });

}



const toggleButton = document.getElementById('toggle-button');
const myDiv = document.getElementById('process-container');

toggleButton.addEventListener('click', () => {
    if (myDiv.style.display === 'none') {
        myDiv.style.display = 'block';
    } else {
        myDiv.style.display = 'none';
    }
});