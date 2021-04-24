import path from 'path';
import {execSync} from 'child_process';
import source from 'shell-source';

const sourceRos = async () => {
    return new Promise<NodeJS.ProcessEnv>((resolve, reject) => {
        source(path.resolve('../ros/devel/setup.bash'), err => {
            if (err) reject(process.env);
            resolve(process.env);
        });
    })
}

const setupRos = async () => {
    process.chdir('./ros');
    
    execSync('catkin_make');

    await sourceRos();

    process.chdir('../');
}

export default setupRos;