import * as React from 'react';
import Servo from './components/Servo/Servo';
import ThrusterInfo from './components/Thrusters/ThrusterInfo/ThrusterInfo';
import Log from './components/Log/Log';
import Camera from './components/Camera/Camera';
import ThrustTweaker from './components/Thrusters/Tweaker/ThrustTweaker';
import IMU from './components/IMU/IMU';
import Compensator from './components/Compensator/Compensator';
import CoM from './components/CoM/CoM';
import Switch from './components/Switch/Switch';


const MainWindow: React.FC = () => {
    return(
        <main>
            <div className="left-column">

                <Servo/>
                <ThrustTweaker/>
                <Compensator/>
                <CoM/>
                <Switch/>

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