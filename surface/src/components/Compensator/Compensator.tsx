import { ipcRenderer } from 'electron';
import * as React from 'react';
import Slider from '../Slider/Slider';

const Compensator: React.FC = () => {
    const [values, setValues] = React.useState<Array<number>>([0.0, 0.0, 0.0])

    return(
        <div className='compensator-container'>
            <h3>Buoyancy</h3>
            {values.map((val, idx) => {
                return(
                    <Slider
                        key={idx}
                        callback={(val) => {
                            let temp = [...values];
                            temp[idx] = val;
                            setValues(temp);

                            ipcRenderer.send('')
                        }}
                    />
                )
            })}
        </div>
    )
}

export default Compensator;