import { ipcRenderer } from 'electron';
import * as React from 'react';
import Slider from '../../Slider/Slider';
import './ThrustTweaker.scss';

const updateValue = (key, value) => {
    
}

const Servo: React.FC = () => {
    const [values, setValues] = React.useState([0, 0, 0, 0, 0, 0])

    return(
        <div className='tweaker-container'>
            <div className='tweaker-title'>Thrust Tweaker</div>
            <div className='tweaker-subtitle'>Translation</div>
            <div className='tweaker-subtitle'>Rotation</div>
            <Slider callback={updateValue}/>
            <Slider callback={updateValue}/>
            <Slider callback={updateValue}/>
            <Slider callback={updateValue}/>
            <Slider callback={updateValue}/>
            <Slider callback={updateValue}/>
        </div>
    )
}