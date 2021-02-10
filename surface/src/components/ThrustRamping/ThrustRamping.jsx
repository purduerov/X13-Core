import React from 'react';
import {Col, Row, Container} from 'react-bootstrap';
import {send, rampSender} from './rampSender.js';
import {ipcRenderer} from 'electron';
import {monitor, kill} from './../../tools/procMonitor.js';

export default class ThrustRamping extends React.Component {
	constructor(props) {
		super(props);

		this.state = {ramp: 0.001};

		this.handleChange = this.handleChange.bind(this);
		this.monitor = monitor.bind(this);
		this.kill = kill.bind(this);

		rampSender(this.monitor);

		ipcRenderer.on('kill', (event, args) => {
			console.log('Killing...');
			this.kill();
		});

	}

	handleChange(val){
		this.setState({ramp: val.target.value});
		send(this.state.ramp);
	}


	render() {
		return (
			<Container>
		      <label>Thrust Ramping: {this.state.ramp}</label>
			  <br/>
		      <input type="range" value={this.state.ramp} min={0.001} max={0.03} step={0.0005} onChange={this.handleChange} />
		    </Container>
		);
	}
}
