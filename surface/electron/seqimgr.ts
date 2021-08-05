import path from 'path';
import {spawn} from 'child_process';
import msg, { LOG_ERROR, LOG_SUCCESS } from '../src/components/Log/LogItem';
import {FRAME} from '../src/components/Log/channels';
import net from 'net';
import {ipcMain} from 'electron';

const messager = (win) => {
    let sock = net.connect(11005, undefined, () => {
        win.webContents.send(FRAME, msg('frame_taker', 'Socket connected', LOG_SUCCESS));
    });

    ipcMain.on('take_frame', (e) => {
        try{
            sock.write('FRAME');
        }catch(e){
            win.webContents.send(FRAME, msg('frame_taker', `Error: ${e}`, LOG_ERROR));
        }
    })

    win.on('close', sock.end);
}

const seqimgr = async (win) => {
    let sender = spawn('python3', ['-u', path.resolve(__dirname, '../cv/stream.py')]);

    sender.stderr.on('data', e => win.webContents.send(FRAME, msg('frame_taker', `Error: ${e}`)));

    sender.stdout.on('data', data => {
        win.webContents.send(FRAME, msg('frame_taker', `Data: ${data}`))
        if(`${data}`.includes('ready')){
            messager(win);
        }
    })

    win.on('close', _ => {
        sender.kill('SIGINT');
        sender.kill('SIGINT');
    })
}

export default seqimgr;