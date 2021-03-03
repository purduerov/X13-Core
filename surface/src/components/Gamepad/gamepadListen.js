const { spawn } = require('child_process');
const path = require('path');

var sender = null;

export function send(data){
    msg = ''
    for(let i = 0; i < 6; i++){
        msg += str(data[i])
        if(i != 5) msg += ','
    }
    msg += '\n'
    sender.stdin.write(msg);
}

export function gamepadListen(connected, monitor) {
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
