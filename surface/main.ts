import {app, BrowserWindow , ipcMain} from 'electron';
import setIp from './electron/setIp';
import setupRos from './electron/setupRos';
import {gamepadListener} from './electron/gamepad';
import log from './src/components/Log/LogItem';
import {CATKIN_MAKE} from './src/components/Log/channels';
import servo from './electron/servo';
import thrusters from './electron/thrusters';
import imu from './electron/imu';

const nodeManager = async (win) => {
  
  await setIp(win);
  
  setupRos().then((env) => {
    process.env = env;
    gamepadListener(win);
    win.webContents.send(CATKIN_MAKE, log('catkin_make', 'Built and sourced'));
    /*
    servo(win).catch(e => {
      console.log(e);
    });
    */
    thrusters(win).catch(e => {
      console.log(e);
    });
    imu(win).catch(e => {
      console.log(e);
    })
  }).catch((err) => {
    win.webContents.send(CATKIN_MAKE, log('catkin_make', `Error: ${err}`));
  })
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
  //win.removeMenu();

  ipcMain.on('logger', (e, msg) => {
    if(msg == 'ready') nodeManager(win);
  })
  
}

app.on('ready', createWindow);
