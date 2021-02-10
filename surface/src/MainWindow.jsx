import React, { Component } from 'react';
import Titlebar from './components/Titlebar/Titlebar.jsx';
import {Container, Row, Col, Button} from 'react-bootstrap';
import './MainWindow.css';
import Gamepad from './components/Gamepad/Gamepad.jsx';
import Console from './components/Console/Console.jsx';
import Cube from './components/Cube/Cube.jsx';
import Depth from './components/Depth/Depth.jsx';
import ThrusterInfo from './components/ThrusterInfo/ThrusterInfo.jsx';
import ThrustRamping from './components/ThrustRamping/ThrustRamping.jsx';
import roscore from './rosjs/roscore.js';
import cleanEnv from '../electron/cleanEnv.js';

export default class MainWindow extends Component {
	constructor(props) {
		super(props);

		this.state = {depth: 0, output: [], statusUpdates: {'gamepad': false}};
		this.gamepadStateUpdate = this.gamepadStateUpdate.bind(this);

		this.roscore = null;
	}

	pushData(data) {
		this.setState({ output: [...this.state.output, data] });
    }

	gamepadStateUpdate(state){
		let st = this.state.statusUpdates;
		st['gamepad'] = state;
		this.setState({statusUpdates: st});
	}

	//<img src="http://192.168.1.3:8090/test.mjpg"/>

	render() {
		return (
			<Container fluid className='p-0 h-100'>

				<div className='h-100 d-flex flex-column'>

					<Row className='mx-0'>
						<Titlebar statusUpdates={this.state.statusUpdates}/>
					</Row>

					<Row className='mx-0 px-3 pb-1 pt-3' style={{height: '70%'}}>
						<Col className='border'>
							<Gamepad gamepadStateUpdate={this.gamepadStateUpdate}/>
							<Depth/>
							<ThrustRamping/>
						</Col>

						<Col xs={8} className='border mx-3'>
							{/*
							<img width='600px' height='500px' src="http://192.168.1.3:8090/test.mjpg"/>
							<img width='600px' height='500px' src="http://192.168.1.4:8090/test.mjpg"/>
							*/}
							<Cube/>
						</Col>

						<Col className='border'>
							<ThrusterInfo/>
						</Col>
					</Row>

					<Row className='mx-0 p-3 flex-grow-1'>
						<Col className='border'>
							<Console output={this.state.output}/>
						</Col>
					</Row>
				</div>

			</Container>
		);
	}

	launchRoscore(){
		console.log('Launching');
		roscore(this.pushData.bind(this));
	}
}
