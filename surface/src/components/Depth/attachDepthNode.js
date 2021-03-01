const { spawn } = require('child_process');
const path = require('path');

module.exports = function attachDepthNode(callback, monitor) {
    const sensor = spawn('python3', ['-u', path.resolve(__dirname, '../../../ros/src/depth_comm/src/depth.py')]);

    monitor(sensor);

    sensor.stdout.on('data', data => {
        try{
            callback(JSON.parse(data.toString().split('\n')[0]));
        }catch(e){
            console.log('Non-JSON data | ROS depth node likely failed');
        }
    });

    sensor.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
}
