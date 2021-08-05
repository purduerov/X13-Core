import { ipcRenderer } from 'electron';
import * as React from 'react';
import { GamepadParams } from '../../../../electron/gamepad';
import Slider from '../../Slider/Slider';
import './CoM.scss';

interface Props {
    vals: Array<number>
}

const CoM: React.FC<Props> = (props) => {
    const [values, setValues] = React.useState<Array<number>>([0.0, 0.0, 0.0]);

    React.useEffect(() => {
        let temp = [...values];
        temp = props.vals.map((val, idx) => val);
        setValues(temp);
        
        ipcRenderer.send('com_send', temp);
    }, props.vals);

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