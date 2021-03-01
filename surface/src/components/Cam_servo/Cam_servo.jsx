import React from 'react';
import {Col, Row, Container} from 'react-bootstrap';
import {servoSender, send} from './servoSender.js';

export default class Cam_servo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {angle: 100.0};
        this.handleChange=this.handleChange.bind(this);
        servoSender();
    }

    handleChange(val) {
        this.setState({ angle: val.target.value });
        send(this.state.angle);
    }

    render() {
        return (
            <Container>
                <label>Servo Angle: {this.state.angle}</label>
                <br />
                <input type="range" value={this.state.angle} min={12.0} max={120.0} step={5.0} onChange={this.handleChange} />
            </Container>
        )
    }

}