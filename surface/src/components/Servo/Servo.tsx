import { ipcRenderer } from 'electron';
import * as React from 'react';
import Slider from '../Slider/Slider';
import './Servo.scss';

interface State{
    value: number
}

export default class Servo extends React.Component<{}, State>{
    constructor(props){
        super(props);

        this.state = {
            value: 50
        }

        this.updateValue = this.updateValue.bind(this);
    }

    updateValue(value){
        this.setState({value: value});
        ipcRenderer.send('servo_send', value);
    }

    render(){
        return(
            <div className='servo-container'>
                <div className='servo-title'>Camera Angle</div>
                <Slider callback={this.updateValue}/>
                <div className='servo-angle'>{this.state.value}&deg;</div>
            </div>
        )
    }
}