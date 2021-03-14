import React from 'react';
import attachDepthNode from './attachDepthNode.js';
import {ipcRenderer} from 'electron';
import {monitor, kill} from './../../tools/procMonitor.js';
import LinearGauge from "../LinearGauge/LinearGauge.jsx";

export default class Depth extends React.Component {
	constructor(props) {
		super(props);

		this.state = {depth: 0.0};
        this.updateDepth = this.updateDepth.bind(this);

		this.monitor = monitor.bind(this);
		this.kill = kill.bind(this);

        attachDepthNode(this.updateDepth, this.monitor);

		ipcRenderer.on('kill', (event, args) => {
			console.log('Killing...');
			this.kill();
		});
	}

    updateDepth(val){
        this.setState({depth: (Math.round(val * 100) / 100)});
    }


	render() {
		return (
			<LinearGauge value={this.state.depth} name="DPTH"/>
		);
	}
}
