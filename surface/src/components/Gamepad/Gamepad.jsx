import React from 'react';
import {Col, Row, Button} from 'react-bootstrap';
import gamepadListen from './gamepadListen.js';
import {ipcRenderer} from 'electron';
import {monitor, kill} from './../../tools/procMonitor.js';

export default class Gamepad extends React.Component {
	constructor(props) {
		super(props);

		this.state = {gamepad: false};

		this.updateGamepad = this.updateGamepad.bind(this);
		this.monitor = monitor.bind(this);
		this.kill = kill.bind(this);

		gamepadListen(this.updateGamepad, this.monitor);

		ipcRenderer.on('kill', (event, args) => {
			console.log('Killing...');
			this.kill();
		});

	}

	updateGamepad(data){
		if(data == false){
			setTimeout(() => {
				gamepadListen(this.updateGamepad, this.monitor);
			}, 1000);
		}else{
			this.setState({gamepad: true});
			console.log(this.state.gamepad);
			//this.props.updateThrust(this.state.gamepad.RT);
		}
		this.props.gamepadStateUpdate(this.state.gamepad);
	}

	render() {
		return (
			<Col>
				Gamepad
			</Col>
		);
	}
}
