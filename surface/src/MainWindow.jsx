import React, { Component } from 'react';
import Titlebar from './components/Titlebar/Titlebar.jsx';
import {Container, Row, Col, Button} from 'react-bootstrap';
import './MainWindow.css';
import Gamepad from './components/Gamepad/Gamepad.jsx';
import Console from './components/Console/Console.jsx';
import Cube from './components/Cube/Cube.jsx';
import LinearGauge from './components/LinearGauge/LinearGauge.jsx';
import Depth from './components/Depth/Depth.jsx';
import ThrusterInfo from './components/ThrusterInfo/ThrusterInfo.jsx';
import ThrustRamping from './components/ThrustRamping/ThrustRamping.jsx';
import ThrustTweaker from './components/ThrustTweaker/ThrustTweaker.jsx';
import Servo from './components/Servo/Servo.jsx';
import roscore from './rosjs/roscore.js';
import cleanEnv from '../electron/cleanEnv.js';
import Camera from './components/Camera/Camera.jsx';

export default class MainWindow extends Component {
	constructor(props) {
		super(props);

		this.state = {output: [], gamepadStyle: {backgroundColor: '#FF0000'}, activeCamera: 0};
		this.gamepadStatusLogic = this.gamepadStatusLogic.bind(this);

		this.setActiveCamera = this.setActiveCamera.bind(this);
		this.roscore = null;
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

	gamepadStateUpdate(state){
		console.log(state);
		let st = this.state.statusUpdates;
		st['gamepad'] = state;
		this.setState({statusUpdates: st});
	}

	setActiveCamera(idx) {
		console.log("Active camera set to " + idx);
		this.setState({
			activeCamera: idx
		});
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
							<Camera mode="column_box" ac={this.state.activeCamera} activeCamera={this.state.activeCamera} updateActiveCamera={this.setActiveCamera}/>
							<Depth/>
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
							<ThrustTweaker/>
						</Col>
					</Row>

					<Row className='mx-0 p-3 flex-grow-1'>
						<Col className='border'>
							<LinearGauge value={25}/>
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
