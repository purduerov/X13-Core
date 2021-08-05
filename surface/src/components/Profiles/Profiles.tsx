import * as React from 'react';
import './Profiles.scss';
import configs from './configs.json';
import ThrustTweaker from './Tweaker/ThrustTweaker';
import Compensator from './Compensator/Compensator';
import CoM from './CoM/CoM';

interface Config {
    tweaker: Array<number>
    com: Array<number>
    compensator: Array<number>
}

const Profiles: React.FC = () => {
    const [config, setConfig] = React.useState('test_config');

    const updateConfig = (which) => setConfig(which);

    return(
        <div className='profile-container'>
            <ThrustTweaker vals={configs[config].tweaker} 
                           fine={configs[config].fine}
                           mode={configs[config].mode}
                           reverse={configs[config].reverse}
                           lockout={configs[config].lockout}
                           />
            <Compensator vals={configs[config].trim}/>
            <CoM vals={configs[config].com}/>
            
            <select onChange={(v) => updateConfig(v.target.value)}>
                <option value='test_config'>test_config</option>
                <option value='other_config'>other_config</option>
                <option value='seabin'>seabin</option>
                <option value='ghost'>ghost</option>
                <option value='sponge'>sponge</option>
            </select>
        </div>
    )
}

export default Profiles;