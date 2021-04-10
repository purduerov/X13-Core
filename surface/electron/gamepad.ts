import path from 'path';
import {spawn} from 'child_process';
import msg from '../src/components/Log/LogItem';
import {GAMEPAD} from '../src/components/Log/channels';

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
        }
    })

    win.on('close', _ => {
        sender.kill('SIGINT');
        sender.kill('SIGINT');
    })
}