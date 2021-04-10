const { spawn } = require('child_process');
const path = require('path');

module.exports = function thrusterListen(callback, monitor) {
    thrusters = spawn('python3', ['-u', path.resolve(__dirname, '../../../ros/src/thrusters/src/status.py')]);

    monitor(thrusters);

    thrusters.on('exit', code => {
        callback(false);
    });

    thrusters.stdout.on('data', data => {
        try{
            callback(JSON.parse(data.toString().split('\n')[0]));
        }catch(e){
            console.log('Non-JSON data | ROS thruster node likely failed');
        }
    });

    thrusters.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
}
