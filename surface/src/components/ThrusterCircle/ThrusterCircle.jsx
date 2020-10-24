import React from 'react';
import {Col, Row, Container} from 'react-bootstrap';
import './ThrusterCircle.css';

export default class ThrusterCircle extends React.Component {
	constructor(props) {
        super(props);
        
        this.state = {val: props.thrust};

        this.circleStyle = {
            backgroundImage: 'linear-gradient(91deg, transparent 50%, #A2ECFB 50%), linear-gradient(90deg, #A2ECFB 50%, transparent 50%)'
        };

        this.setValue = this.setValue.bind(this);

        const poll = setInterval(() => {
            this.setValue(this.props.thrust * 360);
        }, 100);
    }
    
    setValue(val) {
        if(val <= 180){
            this.circleStyle = {
                backgroundImage: 'linear-gradient(' + (val + 90) +'deg, transparent 50%, #A2ECFB 50%),linear-gradient(90deg, #A2ECFB 50%, transparent 50%)'
            };
        }else{
            this.circleStyle = {
                backgroundImage: 'linear-gradient(' + (val - 90) +'deg, transparent 50%, #39B4CC 50%),linear-gradient(90deg, #A2ECFB 50%, transparent 50%)'
            };
        }     
    }

	render() {
		return (
			<Container>
                <div id="activeBorder" class="active-border" style={this.circleStyle}>
                    <div id="circle" class="circle">
                        <span class="val 360" id="val">{Math.round(this.props.thrust * 100)}%</span>
                    </div>
                </div>
			</Container>
		);
	}
}