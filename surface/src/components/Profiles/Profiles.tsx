import * as React from 'react';
import './Toggle.scss';
import test from './configs/test.json';
import ThrustTweaker from './Tweaker/ThrustTweaker';
import Compensator from './Compensator/Compensator';
import CoM from './CoM/CoM';

const Profiles: React.FC = () => {

    return(
        <div>
            <ThrustTweaker/>
            <Compensator/>
            <CoM/>
        </div>
    )
}

export default Profiles;