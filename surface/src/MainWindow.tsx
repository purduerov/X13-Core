import * as React from 'react';
import Servo from './components/Servo/Servo';
import ThrusterInfo from './components/Thrusters/ThrusterInfo/ThrusterInfo';
import Log from './components/Log/Log';
import Camera from './components/Camera/Camera';
import IMU from './components/IMU/IMU';
import Switch from './components/Switch/Switch';
import Mosaic from './components/Mosaic/Mosaic';
import Profiles from './components/Profiles/Profiles';


const MainWindow: React.FC = () => {
    return(
        <main>
            <div className="left-column">

                <Servo/>
                <Profiles/>
                <Mosaic/>

            </div>
            <div className="center-column">

                <Camera/>

            </div>
            <div className="right-column">

                <ThrusterInfo/>
                <img style={{width: '100%'}} src='./img/tools.png'/>
                

            </div>

            <div className="bottom-column">
                
                <Log/>

            </div>
        </main>
    )
}

export default MainWindow;