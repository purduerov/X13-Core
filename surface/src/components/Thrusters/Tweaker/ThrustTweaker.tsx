import { ipcRenderer } from 'electron';
import * as React from 'react';
import Slider from '../../Slider/Slider';
import './ThrustTweaker.scss';

interface State{
    values: Array<number>
}

export default class Servo extends React.Component<{}, State>{
    constructor(props){
        super(props);

        this.state = {
            values: [0, 0, 0, 0, 0, 0]
        }

        this.updateValue = this.updateValue.bind(this);
    }

    updateValue(value){

    }

    render(){
        return(
            <div className='tweaker-container'>
                <div className='tweaker-title'>Thrust Tweaker</div>
                <div className='tweaker-subtitle'>Translation</div>
                <div className='tweaker-subtitle'>Rotation</div>
                <Slider callback={this.updateValue}/>
                <Slider callback={this.updateValue}/>
                <Slider callback={this.updateValue}/>
                <Slider callback={this.updateValue}/>
                <Slider callback={this.updateValue}/>
                <Slider callback={this.updateValue}/>
            </div>
        )
    }
}