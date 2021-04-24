import path from 'path';
import {spawn} from 'child_process';
import {THRUSTERS} from '../src/components/Log/channels';
import msg from '../src/components/Log/LogItem';

const thrusters = async (win) => {
    let listener = spawn('python3', ['-u', path.resolve(__dirname, '../ros/src/thrusters/src/status.py')]);

    win.webContents.send(THRUSTERS, msg(THRUSTERS, 'Started node'));

    listener.on('exit', code => { 
        win.webContents.send(THRUSTERS, msg(THRUSTERS, 'Node exited'));
    });

    listener.stdout.on('data', data => {
        try{
            let arr: Array<number> = JSON.parse(data.toString().split('\n')[0]);
            win.webContents.send('thrusters', arr);
        }catch(e){
            
        }
        
    })

    listener.stderr.on('data', data => {
        win.webContents.send(THRUSTERS, msg(THRUSTERS, `Error: ${data}`));
    })

    win.on('close', _ => {
        listener.kill('SIGINT');
    })
}

export default thrusters;