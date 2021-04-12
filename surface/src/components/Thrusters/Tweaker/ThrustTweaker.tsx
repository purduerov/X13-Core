import { ipcRenderer } from 'electron';
import * as React from 'react';
import Slider from '../../Slider/Slider';
import './ThrustTweaker.scss';


const ThrustTweaker: React.FC = () => {
    const [values, setValues] = React.useState([4.0, 1.5, 4.0, 1.5, 4.0, 1.5])

    return(
        <div className='tweaker-container'>
            <div className='tweaker-title'>Thrust Tweaker</div>
            <div className='tweaker-subtitle'>Translation</div>
            <div className='tweaker-subtitle'>Rotation</div>
            {values.map((_, idx) => {
                return(
                    <Slider 
                        key={idx} 
                        max={idx % 2 == 0 ? 10.0 : 4.0} 
                        step={idx % 2 == 0 ? 0.5 : 0.1}
                        callback={(val) => {
                            let temp = [...values];
                            temp[idx] = val;
                            setValues(temp);
                        }
                    }/>
                )     
            })}
        </div>
    )
}

export default ThrustTweaker;