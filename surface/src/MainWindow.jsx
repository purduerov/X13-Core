import React, { Component } from 'react';
import attachDepthNode from './components/Depth/attachDepthNode.js';
import Titlebar from './components/Titlebar/Titlebar.jsx';
import {Container, Row, Col} from 'react-bootstrap';
import './MainWindow.css';
import Camera from './components/Camera/Camera.jsx';

export default class MainWindow extends Component {
	constructor(props) {
		super(props);

		this.updateDepth = this.updateDepth.bind(this);
		this.setActiveCamera = this.setActiveCamera.bind(this);
		attachDepthNode(this.updateDepth);
		this.state = {depth: 0,
			activeCamera:0};
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
						<Titlebar/>
					</Row>
					
					<Row className='mx-0 px-3 pb-1 pt-3 h-75'>
						<Col className='border'>
						<Camera mode="column_box" updateActiveCamera={this.setActiveCamera}/>						
						</Col>

						<Col xs={8} className='border mx-3'>
						<Camera mode="main_window" activeCamera={this.state.activeCamera} updateActiveCamera={this.setActiveCamera}/>	
						{/*<Camera mode="all_widescreen" updateActiveCamera={this.setActiveCamera}/>*/}
						</Col>
						
						<Col className='border'>
						
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


