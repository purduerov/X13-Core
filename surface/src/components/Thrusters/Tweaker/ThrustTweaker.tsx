import { ipcRenderer } from 'electron';
import * as React from 'react';
import Slider from '../../Slider/Slider';
import './ThrustTweaker.scss';
import {GamepadParams} from '../../../../electron/gamepad';
import Switch from '../../Switch/Switch';

const TRANSLATION_MAX = 10.0;
const ROTATION_MAX = 4.0;
const TRANSLATION_STEP = 0.5;
const ROTATION_STEP = 0.1

const ThrustTweaker: React.FC = () => {
    const [values, setValues] = React.useState([4.0, 4.0, 4.0, 1.5, 1.5, 1.5]);
    const [reverse, setReverse] = React.useState(false);

    const updateSwitch = () => {
        let params: GamepadParams = {
            type: 'reverse',
            reverse: 'F'
        }
        if(reverse){
            setReverse(false);
        }else{
            setReverse(true)
            params.reverse = 'T'
        }

        ipcRenderer.send('reverse', params);
    }

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
                            
                            let params: GamepadParams = {
                                type: 'scale',
                                values: values
                            }

                            console.log(params.values)

                            ipcRenderer.send('gamepad_sock', params);
                        }
                    }/>
                )     
            })}
            <div className='reverse-container'>
                <Switch callback={updateSwitch} checked={reverse}></Switch>
            </div>     
        </div>
    )
}

export default ThrustTweaker;