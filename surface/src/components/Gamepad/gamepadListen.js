const { spawn } = require('child_process');
const JSONStream = require('JSONStream');
const path = require('path');

module.exports = function gamepadListen(connected, monitor) {
    sender = spawn('python3', ['-u', path.resolve(__dirname, '../../../ros/src/gamepad/src/sender.py')]);

    monitor(sender);

    sender.on('exit', code => {
        //console.log(this.state.gamepad);
        connected(false);
    });

    sender.stdout.pipe(JSONStream.parse()).on('data', data => {
        //console.log(data);
        connected(data);
    });

    /*
    sender.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
        connected(false);
    });
    */
}
