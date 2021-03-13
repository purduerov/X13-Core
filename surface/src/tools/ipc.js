//Helper functions for IPC
//Ivan was here

const net = require('net');
let socket = new net.Socket();

function connect(port){
    setTimeout(() => {
        socket = net.connect(port, 'localhost', () => {
            console.log('socket connected');
        });
        socket.on('error', function(ex) {
            console.log("handled error");
            console.log(ex);
        });
    }, 1000);

}

function send(arr){
    try{
        let str = ''
        for(let i = 0; i < arr.length; i++){
            str += arr[i].toString() + ',';
        }
        str = str.slice(0, -1);
        socket.write(str);
    }catch(e){}
}

module.exports = {
    connect,
    send
}
