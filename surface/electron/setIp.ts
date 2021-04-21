import os from 'os';
import { SET_IP } from 'src/components/Log/channels';
import LogItem from 'src/components/Log/LogItem';

const getIp = () => {
    let inter = os.networkInterfaces();
    let i: Array<os.NetworkInterfaceInfo>

    for(let dev in inter){
        i = inter[dev]!.filter((details) => {
            return details.family == 'IPv4' && !details.internal;
        });

        if(i.length > 0) return i[0].address;
    }

    return 'localhost';
}

const setIp = async (win) => {
    const ip = getIp();

    process.env.ROS_HOSTNAME = ip;
    process.env.ROS_IP = ip;
    process.env.ROS_MASTER_URI = 'http://192.168.1.3:11311';
    log('ip_set', `Found ${ip} as local machine`)

    win.webContents.send(SET_IP, {'ip_set', `Found ${ip} as local machine`});
}

export default setIp;