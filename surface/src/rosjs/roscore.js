const { spawn } = require('child_process');
const path = require('path');

module.exports = function roscore(callback) {
    const core = spawn('roscore');

    console.log('Spawned process... roscore');  

    core.stdout.on('data', data => {
        console.log('stdout: ' + data.toString());
        callback(data.toString());
    });

    core.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
}
