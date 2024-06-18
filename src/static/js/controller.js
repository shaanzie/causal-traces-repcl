const socket = io('http://127.0.0.1:5000');

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
});

socket.on('init', (initParams) => {
    console.log('InitParams: ', initParams);
    InitializeGraph(initParams);
});

socket.on('update', (data) => {
    console.log('Received update: ', data)
});


function InitializeGraph(params) {

    const graphCanvas = document.getElementById('graph');

    new Chart(graphCanvas, {
        type: 'line',
        data: [],
        options: {
            scales: {
                xAxis: {
                    max: params['max_X']
                }
            },
            annotation: {
                annotations: [{
                    type: 'box',
                    drawTime: 'beforeDatasetsDraw',
                    yScaleID: 'y-axis-0',
                    yMin: 0,
                    yMax: 200,
                    backgroundColor: 'rgba(0, 255, 0, 0.1)'
                }]
            }
        }
    });

}