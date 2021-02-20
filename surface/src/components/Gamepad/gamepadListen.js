const { spawn } = require('child_process');
const path = require('path');

module.exports = function gamepadListen(connected, monitor) {
    sender = spawn('python3', ['-u', path.resolve(__dirname, '../../../ros/src/gamepad/src/sender.py')]);

    monitor(sender);

    sender.on('exit', code => {
        //console.log(this.state.gamepad);
        connected(false);
    });

    sender.stdout.on('data', data => {
        try{
            connected(JSON.parse(data));
        }catch(e){
            console.log('Non-JSON data | ROS gamepad node likely failed');
        }
    });

    /*
    sender.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
        connected(false);
    });
    */
}
