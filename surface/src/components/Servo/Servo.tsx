import { ipcRenderer } from 'electron';
import * as React from 'react';
import Slider from '../Slider/Slider';
import './Servo.scss';

const Servo: React.FC = () => {
    const [value, setValue] = React.useState(50);

    return(
        <div className='servo-container'>
            <div className='servo-title'>Camera Angle</div>
            <Slider
                callback={(val) => {
                    setValue(val);
                    ipcRenderer.send('servo_send');
                }}
            />
            <div className='servo-angle'>{value}&deg;</div>
        </div>
    )
}

export default Servo;