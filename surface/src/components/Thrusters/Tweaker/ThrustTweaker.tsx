import { ipcRenderer } from 'electron';
import * as React from 'react';
import Slider from '../../Slider/Slider';
import './ThrustTweaker.scss';

const TRANSLATION_MAX = 10.0;
const ROTATION_MAX = 4.0;
const TRANSLATION_STEP = 0.5;
const ROTATION_STEP = 0.1

const ThrustTweaker: React.FC = () => {
    const [values, setValues] = React.useState([4.0, 4.0, 4.0, 1.5, 1.5, 1.5])

    return(
        <div className='tweaker-container'>
            <div className='tweaker-title'>Thrust Tweaker</div>
            <div className='tweaker-subtitle-left'>Translation</div>
            <div className='tweaker-subtitle-right'>Rotation</div>
            {values.map((v, idx) => {
                return(
                    <Slider 
                        value={v}
                        key={idx} 
                        max={idx < 3 ? TRANSLATION_MAX : ROTATION_MAX} 
                        step={idx < 3 ? TRANSLATION_STEP : ROTATION_STEP}
                        callback={(val) => {
                            let temp = [...values];
                            temp[idx] = val;
                            setValues(temp);

                            ipcRenderer.send('gamepad_sock', values);
                        }
                    }/>
                )     
            })}
        </div>
    )
}

export default ThrustTweaker;