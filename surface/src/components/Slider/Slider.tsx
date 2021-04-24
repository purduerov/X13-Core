import * as React from 'react';
import './Slider.scss';

interface Props{
    vertical?: boolean
    min?: number
    max?: number
    step?: number
    unit?: string
    callback(val: number): void
    value: number
}

const defaultProps: Props = {
    vertical: false,
    min: 0,
    max: 100,
    step: 1,
    callback: (_) => {},
    value: 0,
    unit: ''
}

const Slider: React.FC<Props> = (props) => {
    const [starting, setStarting] = React.useState(0);
    React.useEffect(() => {
        setStarting(Object.assign({}, props).value);
    }, [])
    

    return (
        <div className='slider-container'>
            <div className='slider-top'>
                <span className='slider-range'>{props.min}</span>
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
                <span className='slider-range'>{props.max}</span>
            </div>
            <div className='slider-bottom'>
                <button 
                    className='zero-btn'
                    onClick={() => props.callback(starting)}
                >
                    0
                </button>
                <span style={{textAlign: 'center'}}>{props.value}{props.unit}</span>
            </div>
        </div>
        
    )
}

Slider.defaultProps = defaultProps;

export default Slider;
