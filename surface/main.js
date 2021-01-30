const { app, ipcMain } = require('electron');
const path = require('path');
const createWindow = require('./electron/createWindow.js');
const cleanEnv = require('./electron/cleanEnv.js');
const WATCH_MODE = process.env.NODE_ENV === 'WATCH';

if(WATCH_MODE){
	require('electron-reload')(__dirname, {
		electron: path.join(__dirname, 'node_modules', '.bin', 'electron'),
		hardResetMethod: 'close'
	});
}

cleanEnv();

let windows = [];


function bonk(){
	windows[0].destroy();
}

app.on('ready', () => {
	createWindow(windows, 0);
	process.stdout.write('Created window');

	windows[0].on('close', (event, args) => {
		event.preventDefault();
		windows[0].webContents.send('kill');
		setTimeout(bonk, 500);
	});
});

app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit();
	}
});


/*
OUR CODE

░░░░░░░░░░▀▀▀██████▄▄▄░░░░░░░░░░
░░░░░░░░░░░░░░░░░▀▀▀████▄░░░░░░░
░░░░░░░░░░▄███████▀░░░▀███▄░░░░░
░░░░░░░░▄███████▀░░░░░░░▀███▄░░░
░░░░░░▄████████░░░░░░░░░░░███▄░░
░░░░░██████████▄░░░░░░░░░░░███▌░
░░░░░▀█████▀░▀███▄░░░░░░░░░▐███░
░░░░░░░▀█▀░░░░░▀███▄░░░░░░░▐███░
░░░░░░░░░░░░░░░░░▀███▄░░░░░███▌░
░░░░▄██▄░░░░░░░░░░░▀███▄░░▐███░░
░░▄██████▄░░░░░░░░░░░▀███▄███░░░
░█████▀▀████▄▄░░░░░░░░▄█████░░░░
░████▀░░░▀▀█████▄▄▄▄█████████▄░░
░░▀▀░░░░░░░░░▀▀██████▀▀░░░▀▀██░░
*/
