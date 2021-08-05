import { ipcRenderer } from 'electron';
import { GamepadParams } from '../../../../electron/gamepad';
import * as React from 'react';
import Slider from '../../Slider/Slider';
import './Compensator.scss';

const names = ['X', 'Y', 'Z'];

const Compensator: React.FC = () => {
    const [values, setValues] = React.useState<Array<number>>([0.0, 0.0, 0.0])

    return(
        <div className='compensator-container'>
            <div className='compensator-title'>Buoyancy</div>
            {values.map((val, idx) => {
                return(
                    <Slider
                        value={val}
                        key={idx}
                        min={-5.0}
                        max={5.0}
                        step={0.1}
                        callback={(val) => {
                            let temp = [...values];
                            temp[idx] = val;
                            setValues(temp);

                            let params: GamepadParams = {
                                type: 'trim',
                                values: temp
                            }

                            ipcRenderer.send('compensator', params);
                        }}
                    /> 
                )
            })}
        </div>
    )
}

export default Compensator;