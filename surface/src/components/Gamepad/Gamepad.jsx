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
		/*
		if(data == false){
			gamepadListen(this.updateGamepad, this.monitor);
		}else{
			this.setState({gamepad: true});
			console.log(this.state.gamepad);
			//this.props.updateThrust(this.state.gamepad.RT);
		}
		this.props.gamepadStateUpdate(this.state.gamepad);
		*/
	}

	render() {
		return (
			<Col>
				<Row>A: {this.state.gamepad.A == 1 ? 'X' : '-'}</Row>
				<Row>B: {this.state.gamepad.B == 1 ? 'X' : '-'}</Row>
				<Row>X: {this.state.gamepad.X == 1 ? 'X' : '-'}</Row>
				<Row>Y: {this.state.gamepad.Y == 1 ? 'X' : '-'}</Row>
				<Row>RB: {this.state.gamepad.RB == 1 ? 'X' : '-'}</Row>
				<Row>LB: {this.state.gamepad.LB == 1 ? 'X' : '-'}</Row>
				<Row>RSZ: {this.state.gamepad.RSZ == 1 ? 'X' : '-'}</Row>
				<Row>LSZ: {this.state.gamepad.LSZ == 1 ? 'X' : '-'}</Row>
				<Row>START: {this.state.gamepad.START == 1 ? 'X' : '-'}</Row>
				<Row>XBOX: {this.state.gamepad.XBOX == 1 ? 'X' : '-'}</Row>
				<Row>MENU: {this.state.gamepad.MENU == 1 ? 'X' : '-'}</Row>
				<Row>RSX: {this.state.gamepad.RSX}</Row>
				<Row>RSY: {this.state.gamepad.RSY}</Row>
				<Row>LSX: {this.state.gamepad.LSX}</Row>
				<Row>LSY: {this.state.gamepad.LSY}</Row>
				<Row>RT: {this.state.gamepad.RT}</Row>
				<Row>LT: {this.state.gamepad.LT}</Row>
				<Row>DPADX: {this.state.gamepad.DPADX}</Row>
				<Row>DPADY: {this.state.gamepad.DPADY}</Row>
			</Col>
		);
	}
}
