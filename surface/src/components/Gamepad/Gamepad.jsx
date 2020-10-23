import React from 'react';
import {Col, Row} from 'react-bootstrap';
import gamepadListen from './gamepadListen.js';

export default class Gamepad extends React.Component {
	constructor(props) {
		super(props);

		this.state = {gamepad: 'null'};

		this.updateGamepad = this.updateGamepad.bind(this);
		gamepadListen(this.updateGamepad);
		
	}

	updateGamepad(data){
		console.log(data);
		this.setState({gamepad: data});
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