import React, { Component } from 'react';
import attachDepthNode from './components/Depth/attachDepthNode.js';
import Titlebar from './components/Titlebar/Titlebar.jsx';
import {Container, Row, Col, Button} from 'react-bootstrap';
import './MainWindow.css';
import Gamepad from './components/Gamepad/Gamepad.jsx';
import ThrusterCircle from './components/ThrusterCircle/ThrusterCircle.jsx';
import Console from './components/Console/Console.jsx';
import roscore from './rosjs/roscore.js';
import cleanEnv from '../electron/cleanEnv.js';

export default class MainWindow extends Component {
	constructor(props) {
		super(props);

		this.updateDepth = this.updateDepth.bind(this);

		attachDepthNode(this.updateDepth);
		this.state = {depth: 0, thrust: 0, output: []};

		this.roscore = null;

		this.updateThrust = this.updateThrust.bind(this);
	}

	updateThrust(val){
		this.setState({thrust: val});
	}

	pushData(data) { 
		this.setState({ output: [...this.state.output, data] })
    }

	render() {
		return (
			<Container fluid className='p-0 h-100'>
							
				<div className='h-100 d-flex flex-column'>

					<Row className='mx-0'>
						<Titlebar/>
					</Row>
					
					<Row className='mx-0 px-3 pb-1 pt-3 h-75'>
						<Col className='border'>
							<Gamepad updateThrust={this.updateThrust}></Gamepad>
						</Col>

						<Col xs={8} className='border mx-3'>
						
						</Col>

						<Col className='border'>
							<ThrusterCircle thrust={this.state.thrust}/>

							<Container className='py-2'>
								<Button variant='secondary' onClick={this.launchRoscore.bind(this)}>ROSCore</Button>
							</Container>

							<Container>
								<Button variant='danger' onClick={cleanEnv.bind(this)}>Kill ROS</Button>
							</Container>
							
							
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


