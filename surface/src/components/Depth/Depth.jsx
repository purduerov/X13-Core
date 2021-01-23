import React from 'react';
import {Container, Col, Row} from 'react-bootstrap';
import attachDepthNode from './attachDepthNode.js';
import {ipcRenderer} from 'electron';

export default class Depth extends React.Component {
	constructor(props) {
		super(props);

		this.state = {depth: 0.0};
		this.process = null;
        this.updateDepth = this.updateDepth.bind(this);
		this.monitor = this.monitor.bind(this);
        attachDepthNode(this.updateDepth, this.monitor);

		ipcRenderer.on('kill', (event, args) => {
			console.log('Killing...');
			this.kill();
		});
	}

	monitor(process){
		this.process = process;
	}

	kill(){
		if(this.process){
			this.process.kill('SIGKILL');
		}
	}

    updateDepth(val){
        this.setState({depth: (Math.round(val * 100) / 100)});
    }


	render() {
		return (
			<Container>
                Depth: {this.state.depth}
            </Container>
		);
	}
}
