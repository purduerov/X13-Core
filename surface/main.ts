import {app, BrowserWindow , ipcMain} from 'electron';
import setIp from './electron/setIp';
import setupRos from './electron/setupRos';
import gamepadListener from './electron/gamepad';
import log from './src/components/Log/LogItem';
import {CATKIN_MAKE, IMU, SET_IP, THRUSTERS} from './src/components/Log/channels';
import servo from './electron/servo';
import thrusters from './electron/thrusters';
import imu from './electron/imu';

const nodeManager = async (win) => {
  
  await setIp(win).catch(e => win.webContents.send(SET_IP, log('SetIP', `Error: ${e}`)));
  
  await setupRos().catch(e => win.webContents.send(CATKIN_MAKE, log('catkin_make', `Error: ${e}`)));

  gamepadListener(win);
  win.webContents.send(CATKIN_MAKE, log('catkin_make', 'Built and sourced'));

  //thrusters(win).catch(e => send(THRUSTERS, log('Thrusters', `Error: ${e}`)));

  //imu(win).catch(e => send(IMU, log('IMU', `Error: ${e}`)));
}

const createWindow = () => {
  // Create the browser window.
  let win = new BrowserWindow({
    width: 1920,
    height: 1080,
    webPreferences: {
      nodeIntegration: true,
      webSecurity: false,
      contextIsolation: false,
    }
  });

  // and load the index.html of the app.
  win.loadFile('./index.html');

  ipcMain.on('logger', (e, msg) => nodeManager(win));
}

app.on('ready', createWindow);
