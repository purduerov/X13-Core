const { spawn } = require('child_process');
const JSONStream = require('JSONStream');
const path = require('path');

var sender = null;

export function send(data){
    sender.stdin.write(data.toString() + '\n');
}

export function rampSender() {
    sender = spawn('python3', ['-u', path.resolve(__dirname, '../../../ros/src/ramping/src/sender.py')]);

    sender.stderr.on('data', (data) => {
        //console.error(`stderr: ${data}`);
    });
}
