import React from 'react';
import {Container} from 'react-bootstrap';
import './ThrusterCircle.css';

export default class ThrusterCircle extends React.Component {
	constructor(props) {
        super(props);

        this.circleStyle = {
            backgroundImage: 'linear-gradient(91deg, transparent 50%, #A6A6A6 50%), linear-gradient(90deg, #A6A6A6 50%, transparent 50%)'
        };

        this.setValue = this.setValue.bind(this);
    }

    componentDidUpdate(){
        this.setValue(this.props.thrust);
    }

    setValue(val) {
		const color = '#39B4CC';
		if(val < 0){
			color = '#FF4747';
		}
		val = (Math.abs(val) - 127) / 127;

        if(val <= 180){
            this.circleStyle = {
                backgroundImage: 'linear-gradient(' + (val + 90) +'deg, transparent 50%, #A6A6A6 50%),linear-gradient(90deg, #A6A6A6 50%, transparent 50%)'
            };
        }else{
            this.circleStyle = {
                backgroundImage: 'linear-gradient(' + (val - 90) +'deg, transparent 50%, ' + color + ' 50%),linear-gradient(90deg, #A6A6A6 50%, transparent 50%)'
            };
        }
    }

	render() {
		return (
			<Container>
                <div className='active-border' style={this.circleStyle}>
                    <div className='circle'>
                        <span className='val 360'>{Math.round(((Math.abs(this.props.thrust) - 127) / 127) * 100)}%</span>
                    </div>
                </div>
			</Container>
		);
	}
}
