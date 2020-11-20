const { app } = require('electron');
const path = require('path');
const createWindow = require('./electron/createWindow.js');
const cleanEnv = require('./electron/cleanEnv.js');
const rtsp = require('./electron/startRTSP.js');
const WATCH_MODE = process.env.NODE_ENV === 'WATCH';

if(WATCH_MODE){
	require('electron-reload')(__dirname, {
		electron: path.join(__dirname, 'node_modules', '.bin', 'electron')
	});
}

cleanEnv();

let windows = [];

app.on('ready', () => {
	createWindow(windows, 0);
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
