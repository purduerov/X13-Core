const path = require('path');
const { spawn } = require('child_process');

function cleanEnv () {
    const clean = spawn('pkill', ['-f', 'ros']);
    
    clean.on('exit', (code) => {
        console.log('ROS Environment cleaned...');
    });

    clean.on('close', (code) => {
        console.log('ROS Environment cleaned...');
    });
}

module.exports = cleanEnv;