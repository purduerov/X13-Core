const { spawn } = require('child_process');
const JSONStream = require('JSONStream');
const path = require('path');

module.exports = function gamepadListen(callback) {
    console.log(process.env);
    const sensor = spawn('python3', ['-u', path.resolve(__dirname, '../../../../ros/src/roslib_comm/scripts/gamepad_listener.py')]);

    sensor.stdout.pipe(JSONStream.parse()).on('data', data => {
        console.log(data);
        callback(data);
    });

    sensor.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
}
