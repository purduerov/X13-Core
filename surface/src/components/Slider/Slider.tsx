import * as React from 'react';
import './Slider.scss';

interface Props{
    vertical: boolean
    min: number
    max: number
    callback(val: number): void
}


const Slider: React.FC<Props> = ({min, max, callback}) => {

    const [value, setValue] = React.useState(0);

    return (
        <input 
            type='range' 
            min={min} 
            max={max}
            value={value}
            className='slider'
            onChange={(e) => {
                setValue(parseFloat(e.target.value));
                callback(value);
            }}
        />
    )
}
