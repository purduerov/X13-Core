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

export default async function setupRos() {
    process.chdir('./ros');
    const stdout = execSync('catkin_make');

    let env: NodeJS.ProcessEnv = await sourceRos();

    process.chdir('../');

    return env;
}