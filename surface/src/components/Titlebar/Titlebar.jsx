import React from 'react';
import Timer from '../Timer/Timer.jsx';
import Status from '../Status/Status.jsx';
import './Titlebar.css';
import {Col} from 'react-bootstrap';

export default class Titlebar extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className='title'>
				<Col className='col-align'>
					Purdue ROV Main Screen
				</Col>

				<Col>
					<Status module='Gamepad' status={this.props.statusUpdates}/>
					<Status module='Test 1' status={this.props.statusUpdates}/>
					<Status module='Test 2' status={this.props.statusUpdates}/>
				</Col>

				<Col>
					<Timer/>
				</Col>
			</div>
		);
	}
}
