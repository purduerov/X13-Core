import path from 'path';
import {spawn} from 'child_process';
import msg from '../src/components/Log/LogItem';
import {GAMEPAD} from '../src/components/Log/channels';
import net from 'net';
import { ipcMain } from 'electron';

let socket = new net.Socket();

let timeout = 0;

export async function gamepadListener(win) {
    let sender = spawn('python3', ['-u', path.resolve(__dirname, '../ros/src/gamepad/src/sender.py')]);
    timeout = Date.now();

    sender.on('exit', code => { 
        if(Date.now() - timeout > 1000){
            win.webContents.send(GAMEPAD, msg('gamepad_listener', 'Error! Gamepad lost. Reacquiring...'));
        }
        setTimeout(() => {
            gamepadListener(win);
        }, 1000)   
    });

    sender.stderr.on('data', data => {
        console.log(`Gamepad Listener:\n${data}`);
        win.webContents.send(GAMEPAD, msg('gamepad_listener', `Error: ${data}`));
    })

    sender.stdout.on('data', data => {
        console.log(data.toString());
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

    win.on('close', _ => {
        sender.kill('SIGINT');
        sender.kill('SIGINT');
    })
}