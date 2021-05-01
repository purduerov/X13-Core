import path from 'path';
import {spawn} from 'child_process';
import msg, { LOG_ERROR, LOG_SUCCESS } from '../src/components/Log/LogItem';
import {COM} from '../src/components/Log/channels';
import net from 'net';
import {ipcMain} from 'electron';

const messager = (win) => {
    let sock = net.connect(11003, undefined, () => {
        win.webContents.send(COM, msg('com', 'Socket connected', LOG_SUCCESS));
    });

    ipcMain.on('com_send', (e, data: Array<number>,) => {
        try{
            let str = '';
            for(let v of data) str += `${v.toString()},`;
            str = str.slice(0, -1);
            str += ';';
            sock.write(str);
        }catch(e){
            win.webContents.send(COM, msg('com', `Error: ${e}`, LOG_ERROR));
        }
    })

    win.on('close', sock.end);
}

const com = async (win) => {
    let sender = spawn('python3', ['-u', path.resolve(__dirname, '../ros/src/com_pub/src/sender.py'), '11003']);

    sender.stderr.on('data', e => win.webContents.send(COM, msg('com', `Error: ${e}`)));

    sender.stdout.on('data', data => {
        win.webContents.send(COM, msg('com', `Data: ${data}`))
        if(`${data}`.includes('ready')){
            messager(win);
        }
    })

    win.on('close', _ => {
        sender.kill('SIGINT');
        sender.kill('SIGINT');
    })
}

export default com;