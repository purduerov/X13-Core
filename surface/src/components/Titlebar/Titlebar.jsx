import React from 'react';
import Timer from '../Timer/Timer.jsx';
import Status from '../Status/Status.jsx';
import './Titlebar.css';
import {Col} from 'react-bootstrap';

export default class Titlebar extends React.Component {
	constructor(props) {
		super(props);
		this.state = {statusUpdates: this.props.statusUpdates};
		this.gamepadStatusLogic = this.gamepadStatusLogic.bind(this);
	}

	gamepadStatusLogic(){
		if(this.state.statusUpdates['gamepad']){
			return {backgroundColor: '#00FF00'};
		}
		return {backgroundColor: '#FF0000'};
	}

	render() {
		return (
			<div className='title'>
				<Col className='col-align'>
					Purdue ROV Main Screen
				</Col>

				<Col>
					<Status module='Gamepad' status={this.gamepadStatusLogic}/>
					<Status module='Test 1' status={this.gamepadStatusLogic}/>
					<Status module='Test 2' status={this.gamepadStatusLogic}/>
				</Col>

				<Col>
					<Timer/>
				</Col>
			</div>
		);
	}
}
