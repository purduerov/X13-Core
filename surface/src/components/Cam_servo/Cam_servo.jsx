import React from 'react';
import {Col, Row, Container} from 'react-bootstrap';
import {servoSender, send} from './servoSender.js';
import {monitor, kill} from './../../tools/procMonitor.js';
import {ipcRenderer} from 'electron';

export default class Cam_servo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {angle: 30.0};
        this.handleChange=this.handleChange.bind(this);

        this.monitor = monitor.bind(this);
		this.kill = kill.bind(this);

        servoSender(this.monitor);

        ipcRenderer.on('kill', (event, args) => {
			console.log('Killing...');
			this.kill();
		});
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
                <input type="range" value={this.state.angle} min={0.0} max={180.0} step={5.0} onChange={this.handleChange} />
            </Container>
        )
    }

}
