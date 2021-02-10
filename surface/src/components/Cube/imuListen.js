const { spawn } = require('child_process');
const JSONStream = require('JSONStream');
const path = require('path');

module.exports = function imuListen(callback, monitor) {
    sender = spawn('python3', ['-u', path.resolve(__dirname, '../../../ros/src/imu/src/status.py')]);

    monitor(sender);

    sender.on('exit', code => {
        callback(false);
    });

    sender.stdout.pipe(JSONStream.parse()).on('data', data => {
        //console.log(data);
        callback(data);
    });

    sender.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
}
