import { ipcRenderer } from 'electron';
import * as React from 'react';
import Slider from '../../Slider/Slider';
import './CoM.scss';

const names = ['X', 'Y', 'Z'];

const CoM: React.FC = () => {
    const [values, setValues] = React.useState<Array<number>>([0.0, 0.0, 0.0])

    return(
        <div className='com-container'>
            <div className='com-title'>CoM</div>
            {values.map((val, idx) => {
                return(
                    <Slider
                        value={val}
                        key={idx}
                        min={-2.0}
                        max={2.0}
                        step={0.01}
                        callback={(val) => {
                            let temp = [...values];
                            temp[idx] = val;
                            setValues(temp);

                            ipcRenderer.send('com_send', temp);
                        }}
                    /> 
                )
            })}
        </div>
    )
}

export default CoM;