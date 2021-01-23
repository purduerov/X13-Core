const { spawn } = require('child_process');
const JSONStream = require('JSONStream');
const path = require('path');

module.exports = function gamepadListen(callback) {
    sender = spawn('python3', ['-u', path.resolve(__dirname, '../../../ros/src/gamepad/src/sender.py')]);

    sender.on('exit', code => {
        //console.log(this.state.gamepad);
        callback(false);
    });

    sender.stdout.pipe(JSONStream.parse()).on('data', data => {
        //console.log(data);
        callback(data);
    });

    sender.stderr.on('data', (data) => {
        //console.error(`stderr: ${data}`);
        callback(false);
    });
}
