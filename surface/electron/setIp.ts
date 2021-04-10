import os from 'os';

async function getIp() {
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

export default async function setIp(){
    const ip = await getIp();

    process.env.ROS_HOSTNAME = ip;
    process.env.ROS_IP = ip;
    process.env.ROS_MASTER_URI = 'http://192.168.1.3:11311';

    return ip;
}