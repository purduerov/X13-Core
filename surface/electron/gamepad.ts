import path from 'path';
import {spawn} from 'child_process';
import msg from '../src/components/Log/LogItem';
import {GAMEPAD} from '../src/components/Log/channels';
import net from 'net';
import { ipcMain } from 'electron';

let socket = new net.Socket();

let sender;

const wait = async (win) => {
    let promise = new Promise((resolve, reject) => {
        setTimeout(() => resolve('spawn again'), 1000);
    });
    await promise;

    gamepadListener(win);
}

const kill = () => {
    sender.kill('SIGINT');
    sender.kill('SIGINT');
}

const gamepadListener = async (win: Electron.BrowserWindow) => {
    win.on('close', kill);

    sender = spawn('python3', ['-u', path.resolve(__dirname, '../ros/src/gamepad/src/sender.py')]);

    sender.on('exit', _ => {
        wait(win);
        win.removeListener('close', kill);
    });

    sender.stderr.on('data', data => {
        win.webContents.send(GAMEPAD, msg('gamepad_listener', `Error: ${data}`));
    });

    sender.stdout.on('data', data => {
        if(`${data}`.includes('ready')){
            win.webContents.send(GAMEPAD, msg('gamepad_listener', 'Gamepad connected'));
            socket = net.connect(11001, 'localhost', () => {
                win.webContents.send(GAMEPAD, msg('gamepad_listener', 'Socket connected'));
            })

            socket.on('error', (err) => {
                win.webContents.send(GAMEPAD, msg('gamepad_listener', 'Socket error'));
            })

            ipcMain.on('gamepad_sock', (e, arr) => {
                try{
                    let str = ''
                    for(let i = 0; i < arr.length; i++){
                        str += arr[i].toString() + ',';
                    }
                    str = str.slice(0, -1);
                    socket.write(str);
                }catch(e){
                    win.webContents.send(GAMEPAD, msg('gamepad_listener', 'Socket write error'));
                }
            })
        }
    })
}

export default gamepadListener;