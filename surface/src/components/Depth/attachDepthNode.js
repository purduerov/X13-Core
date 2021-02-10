const { spawn } = require('child_process');
const JSONStream = require('JSONStream');
const path = require('path');

module.exports = function attachDepthNode(callback, monitor) {
    const sensor = spawn('python3', ['-u', path.resolve(__dirname, '../../../ros/src/depth_comm/src/depth.py')]);

    monitor(sensor);

    sensor.stdout.pipe(JSONStream.parse()).on('data', data => {
        callback(data);
    });

    sensor.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
}
