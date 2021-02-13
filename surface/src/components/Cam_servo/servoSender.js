const { spawn } = require('child_process');
const JSONStream = require('JSONStream');
const path = require('path');

var sender = null;

export function send(data){
    sender.stdin.write(data.toString() + '\n');
}

export function servoSender(monitor) {
    sender = spawn('python3', ['-u', path.resolve(__dirname, '../../../ros/src/cam_servo/src/servo_sender.py')]);

    monitor(sender);
}
