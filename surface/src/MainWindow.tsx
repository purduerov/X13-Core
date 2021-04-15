import * as React from 'react';
import Servo from './components/Servo/Servo';
import ThrusterInfo from './components/Thrusters/ThrusterInfo/ThrusterInfo';
import Log from './components/Log/Log';
import Camera from './components/Camera/Camera';
import ThrustTweaker from './components/Thrusters/Tweaker/ThrustTweaker';
import IMU from './components/IMU/IMU';
import Compensator from './components/Compensator/Compensator';


const MainWindow: React.FC = () => {
    return(
        <main>
            <div className="left-column">

                <Servo/>
                <ThrustTweaker/>
                <Compensator/>

            </div>
            <div className="center-column">

                <Camera/>

            </div>
            <div className="right-column">

                <ThrusterInfo/>
                <IMU/>

            </div>

            <div className="bottom-column">
                
                <Log/>

            </div>
        </main>
    )
}

export default MainWindow;