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
import Servo from './components/Servo/Servo.jsx';
import roscore from './rosjs/roscore.js';
import cleanEnv from '../electron/cleanEnv.js';
import Camera from './components/Camera/Camera.jsx';
import {connect, send} from './tools/ipc.js';

export default class MainWindow extends Component {
	constructor(props) {
		super(props);

		this.state = {output: [], gamepadStyle: {backgroundColor: '#FF0000'}, activeCamera: 0, constants: [4.0, 4.0, 4.0, 1.0, 1.0, 1.0]};
		this.gamepadStatusLogic = this.gamepadStatusLogic.bind(this);

		this.setActiveCamera = this.setActiveCamera.bind(this);

		this.roscore = null;

		connect(11001);
	}

	pushData(data) {
		this.setState({ output: [...this.state.output, data] });
    }

	gamepadStatusLogic(state){
		if(state){
			this.setState({gamepadStyle: {backgroundColor: '#00FF00'}});
		}else{
			this.setState({gamepadStyle: {backgroundColor: '#FF0000'}});
		}
	}

	setActiveCamera(idx) {
		console.log("Active camera set to " + idx);
		this.setState({
			activeCamera: idx
		});
	}

	handleConstants(e, a){
		let st = this.state.constants;
		st[a] = e.target.value;
		this.setState({constants: st});

		send(this.state.constants);
		//Socket stuff here
	}

	render() {

		return (
			<Container fluid className='p-0 h-100'>

				<div className='h-100 d-flex flex-column'>

					<Row className='mx-0'>
						<Titlebar statusUpdates={this.state.gamepadStyle}/>
					</Row>

					<Row className='mx-0 px-3 pb-1 pt-3' style={{height: '70%'}}>
						<Col className='border'>
							<Camera mode="column_box" updateActiveCamera={this.setActiveCamera}/>
							<Depth/>
							<ThrustRamping/>
							<Servo/>
							<Gamepad ref={this.gamepad} status={this.gamepadStatusLogic}/>
						</Col>

						<Col xs={8} className='border mx-3'>
							{/*
							<img width='600px' height='500px' src="http://192.168.1.3:8090/test.mjpg"/>
							<img width='600px' height='500px' src="http://192.168.1.4:8090/test.mjpg"/>
							*/}


							<Camera mode="main_window" activeCamera={this.state.activeCamera} updateActiveCamera={this.setActiveCamera}/>
						</Col>

						<Col className='border'>
							<ThrusterInfo/>
							<input type="range" value={this.state.constants[0]} min={0.0} max={10.0} step={0.1} onChange={(e) => {this.handleConstants(e, 0)}} />
							<input type="range" value={this.state.constants[1]} min={0.0} max={10.0} step={0.1} onChange={(e) => {this.handleConstants(e, 1)}} />
							<input type="range" value={this.state.constants[2]} min={0.0} max={10.0} step={0.1} onChange={(e) => {this.handleConstants(e, 2)}} />
							<input type="range" value={this.state.constants[3]} min={0.0} max={2.0} step={0.1} onChange={(e) => {this.handleConstants(e, 3)}} />
							<input type="range" value={this.state.constants[4]} min={0.0} max={2.0} step={0.1} onChange={(e) => {this.handleConstants(e, 4)}} />
							<input type="range" value={this.state.constants[5]} min={0.0} max={2.0} step={0.1} onChange={(e) => {this.handleConstants(e, 5)}} />
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
