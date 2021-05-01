import path from 'path';
import {spawn} from 'child_process';
import {IMU} from '../src/components/Log/channels';
import msg, { LOG_ERROR, LOG_WARNING } from '../src/components/Log/LogItem';

export default async function imu(win) {
    let listener = spawn('python3', ['-u', path.resolve(__dirname, '../ros/src/imu/src/status.py')]);

    win.webContents.send(IMU, msg('imu', 'Started node'));

    listener.on('exit', code => { 
        win.webContents.send(IMU, msg('imu', 'Node exited', LOG_WARNING));
    });

    listener.stdout.on('data', data => {
        try{
            let arr: Array<number> = JSON.parse(data.toString().split('\n')[0]);
            win.webContents.send('imu', arr);
        }catch(e){
            console.log(e);
        }
        
    })

    listener.stderr.on('data', data => {
        win.webContents.send(IMU, msg('imu', `Error: ${data}`, LOG_ERROR));
    })

    win.on('close', _ => {
        listener.kill('SIGINT');
    })
}