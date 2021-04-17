import * as React from 'react';
import './ThrusterCircle.scss';

interface Props{
    thrust: number
    className: string
    name: string
}

const l180 = (val: number) => {
    return({
        backgroundImage:
            `linear-gradient(${val + 90}deg, transparent 50%, #A6A6A6 50%),` +
            `linear-gradient(90deg, #A6A6A6 50%, transparent 50%)`
    })
}

const g180 = (val: number, original: number) => {
    return({
        backgroundImage:
            `linear-gradient(${val - 90}deg, transparent 50%, ${original < 127 ? '#FF4747' : '#39B4CC'} 50%),` +
            `linear-gradient(90deg, #A6A6A6 50%, transparent 50%)`
    })
}

const ThrusterCircle: React.FC<Props> = (props) => {
    const [angle, setAngle] = React.useState(Math.round(((Math.abs(props.thrust) - 127) / 127) * 360));
    
    React.useEffect(() => {
        setAngle(Math.round(((Math.abs(props.thrust) - 127) / 127) * 360))
    }, [props.thrust]);
    
    return(
        <div className={props.className}>
            <div className='active-border' style={angle <= 180 ? l180(angle) : g180(angle, props.thrust)}>
                <div className='circle'>
                    <span className='val 360'>{Math.round(angle / 360 * 100)}%</span>
                    <br/>
                    <span className='val 360'>{props.name}</span>
                </div>
            </div>
        </div>
    )
}

export default ThrusterCircle;