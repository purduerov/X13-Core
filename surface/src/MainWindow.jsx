import React, { Component } from 'react';
import attachDepthNode from './components/Depth/attachDepthNode.js';
import Titlebar from './components/Titlebar/Titlebar.jsx';
import {Container, Row, Col, Button} from 'react-bootstrap';
import './MainWindow.css';
import Gamepad from './components/Gamepad/Gamepad.jsx';
import ThrusterCircle from './components/ThrusterCircle/ThrusterCircle.jsx';
import Console from './components/Console/Console.jsx';
import Cube from './components/Cube/Cube.jsx';
import roscore from './rosjs/roscore.js';
import cleanEnv from '../electron/cleanEnv.js';
import thrusterListen from './components/ThrusterCircle/thrusterListen.js';

export default class MainWindow extends Component {
	constructor(props) {
		super(props);

		this.updateDepth = this.updateDepth.bind(this);

		attachDepthNode(this.updateDepth);
		this.state = {depth: 0, thrust: [127, 127, 127, 127, 127, 127, 127, 127], output: []};

		this.roscore = null;

		this.updateThrust = this.updateThrust.bind(this);
		thrusterListen(this.updateThrust);
	}

	modifyValues(vals){
		const list = this.state.thrust.map((t, idx) => vals[idx]);

		return list;
	}

	updateThrust(data){
		this.setState({thrust: this.modifyValues(data)});
	}

	pushData(data) {
		this.setState({ output: [...this.state.output, data] });
    }

	//<img src="http://192.168.1.3:8090/test.mjpg"/>

	render() {
		return (
			<Container fluid className='p-0 h-100'>

				<div className='h-100 d-flex flex-column'>

					<Row className='mx-0'>
						<Titlebar/>
					</Row>

					<Row className='mx-0 px-3 pb-1 pt-3 h-75'>
						<Col className='border'>
							<Gamepad></Gamepad>
						</Col>

						<Col xs={8} className='border mx-3'>
							<img src="http://192.168.1.3:8090/test.mjpg"/>
						</Col>

						<Col className='border'>
							<ThrusterCircle thrust={this.state.thrust[0]} top={-40 + 50} left={-110 + 130}/>
							<ThrusterCircle thrust={this.state.thrust[4]} top={40 + 50} left={-80 + 130}/>
							<ThrusterCircle thrust={this.state.thrust[1]} top={-40 + 50} left={60 + 130}/>
							<ThrusterCircle thrust={this.state.thrust[5]} top={40 + 50} left={30 + 130}/>
							<ThrusterCircle thrust={this.state.thrust[7]} top={125 + 50} left={-80 + 130}/>
							<ThrusterCircle thrust={this.state.thrust[3]} top={205 + 50} left={-110 + 130}/>
							<ThrusterCircle thrust={this.state.thrust[6]} top={125 + 50} left={30 + 130}/>
							<ThrusterCircle thrust={this.state.thrust[2]} top={205 + 50} left={60 + 130}/>

							<Cube/>



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

	updateDepth(newVal) {
		this.setState({depth: newVal});
	}
}
