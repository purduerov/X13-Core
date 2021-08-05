import { ipcRenderer } from 'electron';
import * as React from 'react';
import Slider from '../../Slider/Slider';
import './ThrustTweaker.scss';
import {GamepadParams} from '../../../../electron/gamepad';
import Toggle from '../../Toggle/Toggle';

const TRANSLATION_MAX = 1.0;
const ROTATION_MAX = 1.0;
const TRANSLATION_STEP = 0.05;
const ROTATION_STEP = 0.05;

const ThrustTweaker: React.FC = () => {
    const [values, setValues] = React.useState([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]);
    const [fine, setFine] = React.useState(1.041)
    const [reverse, setReverse] = React.useState(false);
    const [mode, setMode] = React.useState(true);
    const [lockout, setLockout] = React.useState(true);

    const updateSwitch = () => {
        let params: GamepadParams = {
            type: 'reverse',
            reverse: 'F'
        }

        if(!reverse){
            params.reverse = 'T';
        }
        
        setReverse(!reverse);

        ipcRenderer.send('reverse', params);
    }

    const updateMode = () => {
        let params: GamepadParams = {
            type: 'mode',
            reverse: 'F'
        }

        if(!mode){
            params.mode = 'T';
        }
        
        setMode(!mode);

        ipcRenderer.send('mode', params);
    }

    const updateLockout = () => {
        let params: GamepadParams = {
            type: 'lockout',
            lockout: 'F'
        }

        if(!lockout){
            params.lockout = 'T';
        }
        
        setLockout(!lockout);

        ipcRenderer.send('lockout', params);
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
                <Toggle toggled={reverse} callback={updateSwitch} name='Reverse'/>
                <Toggle toggled={mode} callback={updateMode} name='Fine'/>
                <Toggle toggled={lockout} callback={updateLockout} name='Yeeter Lockout'/>
            </div>   
            <div className='fine-slider'>  
            <Slider
                value={fine}
                key={10}
                max={5}
                step={0.01}
                callback={(val) => {
                    setFine(val);

                    let params: GamepadParams = {
                        type: 'absolute',
                        values: [val]
                    }
            
                    ipcRenderer.send('absolute', params);
                }}/>
            </div>
        </div>
    )
}

export default ThrustTweaker;