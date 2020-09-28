import React, { Component } from 'react';
import attachDepthNode from './components/depth/attachDepthNode.js';

export default class MainWindow extends Component {
	constructor(props) {
		super(props);

		this.updateDepth = this.updateDepth.bind(this);

		attachDepthNode(this.updateDepth);
		this.state = {depth: 0};
	}

	render() {
		return (
			<div>
				<h1>{this.state.depth}</h1>
			</div>		
		);
	}

	updateDepth(newVal) {
		this.setState({depth: newVal});
	}
}


