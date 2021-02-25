const { spawn } = require('child_process');
const path = require('path');

module.exports = function imuListen(callback, monitor) {
    imu = spawn('python3', ['-u', path.resolve(__dirname, '../../../ros/src/imu/src/status.py')]);

    monitor(imu);

    imu.on('exit', code => {
        callback(false);
    });

    imu.stdout.on('data', data => {
        try{
            callback(JSON.parse(data.toString().split('\n')[0]));
        }catch(e){
            console.log('Non-JSON data | ROS IMU node likely failed');
        }
    });

    imu.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
}
