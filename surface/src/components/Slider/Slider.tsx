import * as React from 'react';
import './Slider.scss';

interface Props{
    vertical: boolean
    min: number
    max: number
    callback(val: number): void
}

const defaultProps: Props = {
    vertical: false,
    min: 0,
    max: 100,
    callback: (_) => {}
}


const Slider: React.FC<Props> = (props) => {

    const [value, setValue] = React.useState(0);

    return (
        <input 
            type='range' 
            min={props.min} 
            max={props.max}
            value={value}
            className='slider'
            onChange={(e) => {
                setValue(parseFloat(e.target.value));
                props.callback(value);
            }}
        />
    )
}
