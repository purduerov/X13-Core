import path from 'path';
import {spawn} from 'child_process';
import msg from '../src/components/Log/LogItem';
import {SERVO} from '../src/components/Log/channels';
import net from 'net';
import {ipcMain} from 'electron';

const messager = (win) => {
    let sock = net.connect(11002, undefined, () => {
        win.webContents.send(SERVO, msg('servo', 'Socket connected'));
    });

    ipcMain.on('servo_send', (e, data: number,) => {
        sock.write(`${data}`);
    })

    sock.on('error', _ => win.webContents.send(SERVO, msg('servo', 'Socket error!')));

    win.on('close', _ => {
        sock.end();
    })
}

const servo = async (win) => {
    let sender = spawn('python3', ['-u', path.resolve(__dirname, '../ros/src/cam_servo/src/servo_sender.py'), '11002']);
    
    win.webContents.send(SERVO, msg('servo', 'Started'));

    sender.on('exit', code => { 
        win.webContents.send(SERVO, msg('servo', 'Exiting...'));
    });

    sender.stdout.on('data', data => {
        if(`${data}`.includes('ready')){
            messager(win);
        }
    })

    sender.stderr.on('data', data => {
        win.webContents.send(SERVO, msg('servo', `Error: ${data}`));
    })

    win.on('close', _ => {
        sender.kill('SIGINT');
        sender.kill('SIGINT');
    })
}

export default servo;