import path from 'path';
import {spawn} from 'child_process';
import msg, { LOG_ERROR, LOG_SUCCESS, LOG_WARNING } from '../src/components/Log/LogItem';
import {GAMEPAD} from '../src/components/Log/channels';
import net from 'net';
import { ipcMain } from 'electron';
import { values } from 'webpack.config';

export interface GamepadParams {
    type: 'trim' | 'scale' | 'reverse'
    reverse?: string
    values?: Array<number>
}

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
        win.webContents.send(GAMEPAD, msg('gamepad_listener', `Error: ${data}`, LOG_ERROR));
    });

    sender.stdout.on('data', data => {
        if(`${data}`.includes('ready')){
            win.webContents.send(GAMEPAD, msg('gamepad_listener', 'Gamepad connected', LOG_SUCCESS));
            socket = net.connect(11001, 'localhost', () => {
                win.webContents.send(GAMEPAD, msg('gamepad_listener', 'Socket connected', LOG_SUCCESS));
            })

            socket.on('error', (err) => {
                win.webContents.send(GAMEPAD, msg('gamepad_listener', 'Socket error', LOG_ERROR));
            })

            ipcMain.on('gamepad_sock', (e, params: GamepadParams) => {
                try{
                    let str = `${params.type}:`
                    for(let v of params.values!) str += `${v.toString()},`;
                    str = str.slice(0, -1);
                    socket.write(str);
                }catch(e){
                    win.webContents.send(GAMEPAD, msg('gamepad_listener', 'Socket write error', LOG_ERROR));
                }
            })

            ipcMain.on('compensator', (e, params: GamepadParams) => {
                try{
                    let str = `${params.type}:`
                    for(let v of params.values!) str += `${v.toString()},`;
                    str = str.slice(0, -1);
                    socket.write(str);
                }catch(e){
                    win.webContents.send(GAMEPAD, msg('gamepad_listener', 'Socket write error', LOG_ERROR));
                }
            })

            ipcMain.on('reverse', (e, params: GamepadParams) => {
                try{
                    let str = `${params.type}:${params.reverse!}`
                    socket.write(str);
                }catch(e){
                    win.webContents.send(GAMEPAD, msg('gamepad_listener', 'Socket write error', LOG_ERROR));
                }
            })
        }

        win.webContents.send(GAMEPAD, msg('gamepad_listener', `Data: ${data}`, LOG_WARNING));
    })
}

export default gamepadListener;