import * as React from 'react';
import './Slider.scss';

interface Props{
    vertical?: boolean
    min?: number
    max?: number
    step?: number
    callback(val: number): void
    value: number
}

const defaultProps: Props = {
    vertical: false,
    min: 0,
    max: 100,
    step: 1,
    callback: (_) => {},
    value: 0
}


const Slider: React.FC<Props> = (props) => {

    const [value, setValue] = React.useState(0);

    return (
        <input 
            type='range' 
            min={props.min} 
            max={props.max}
            value={props.value}
            step={props.step}
            className='slider'
            onChange={(e) => {
                props.callback(parseFloat(e.target.value));
            }}
        />
    )
}

Slider.defaultProps = defaultProps;

export default Slider;
