//Helper functions for tracking and killing processes
//Ivan was here

function monitor(process){
    this.process = process;
}

function kill(){
    if(this.process){
        this.process.kill('SIGKILL');
    }
}

module.exports = {
    monitor,
    kill
}
