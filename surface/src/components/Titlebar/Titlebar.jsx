import React from 'react';
import Timer from '../Timer/Timer.jsx';
import Status from '../Status/Status.jsx';
import './Titlebar.css';
import {Col} from 'react-bootstrap';

export default class Titlebar extends React.Component {
	constructor(props) {
		super(props);
		this.state = {status_states: this.props.status_states};
	}

	render() {
		return (
			<div className='title'>
				<Col className='col-align'>
					Purdue ROV Main Screen
				</Col>

				<Col>
					<Status module='Gamepad' status={this.state.status_states['gamepad']}/>
					<Status module='Test 1' status={true}/>
					<Status module='Test 2' status={false}/>
				</Col>

				<Col>
					<Timer/>
				</Col>
			</div>
		);
	}
}
