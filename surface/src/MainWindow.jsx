import React, { Component } from 'react';
import attachDepthNode from './components/Depth/attachDepthNode.js';
import Titlebar from './components/Titlebar/Titlebar.jsx';

export default class MainWindow extends Component {
	constructor(props) {
		super(props);

		this.updateDepth = this.updateDepth.bind(this);

		attachDepthNode(this.updateDepth);
		this.state = {depth: 0};
	}

	render() {
		return (
			<div className='container-fluid p-0'>
				<Titlebar/>
				<div>
					<h1>{this.state.depth}</h1>
				</div>
			</div>			
		);
	}

	updateDepth(newVal) {
		this.setState({depth: newVal});
	}
}


