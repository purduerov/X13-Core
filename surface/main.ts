import {app, BrowserWindow , ipcMain} from 'electron';
import setIp from './electron/setIp';
import setupRos from './electron/setupRos';
import gamepadListener from './electron/gamepad';
import log, { LOG_SUCCESS } from './src/components/Log/LogItem';
import {CATKIN_MAKE, GENERAL, IMU, SERVO, SET_IP, THRUSTERS} from './src/components/Log/channels';
import servo from './electron/servo';
import thrusters from './electron/thrusters';
import imu from './electron/imu';
import com from './electron/com';

const nodeManager = async (win: BrowserWindow) => {
  
  await setIp(win).catch(e => win.webContents.send(SET_IP, log('SetIP', `Error: ${e}`)));
  
  await setupRos().catch(e => win.webContents.send(CATKIN_MAKE, log('catkin_make', `Error: ${e}`)));

  gamepadListener(win);
  win.webContents.send(CATKIN_MAKE, log('catkin_make', 'Built and sourced'));

  servo(win).catch(e => win.webContents.send(SERVO, `Error: ${e}`));

  thrusters(win).catch(e => win.webContents.send(THRUSTERS, log('Thrusters', `Error: ${e}`)));

  imu(win).catch(e => win.webContents.send(IMU, log('IMU', `Error: ${e}`)));

  com(win);
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

  ipcMain.on('logger', (e, msg) => {
    e.sender.send(GENERAL, log('General', 'Welcome!', LOG_SUCCESS));
    e.sender.send(GENERAL, log('General', 'Pilot Interface Starting...'));
  })

  if(process.env.NODE_ENV !== 'development'){
    ipcMain.on('logger', (e, msg) => nodeManager(win));
  } 
}

app.on('ready', createWindow);
