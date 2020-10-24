import React, { Component } from 'react';
import attachDepthNode from './components/Depth/attachDepthNode.js';
import Titlebar from './components/Titlebar/Titlebar.jsx';
import {Container, Row, Col} from 'react-bootstrap';
import './MainWindow.css';
import Gamepad from './components/Gamepad/Gamepad.jsx';
import ThrusterCircle from './components/ThrusterCircle/ThrusterCircle.jsx';

export default class MainWindow extends Component {
	constructor(props) {
		super(props);

		this.updateDepth = this.updateDepth.bind(this);

		attachDepthNode(this.updateDepth);
		this.state = {depth: 0, thrust: 0};

		this.updateThrust = this.updateThrust.bind(this);
	}

	updateThrust(val){
		this.setState({thrust: val});
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
						</Col>
					</Row>

					<Row className='mx-0 p-3 flex-grow-1'>
						<Col className='border'>
							
						</Col>
					</Row>
				</div>						
				
			</Container>			
		);
	}

	updateDepth(newVal) {
		this.setState({depth: newVal});
	}
}


