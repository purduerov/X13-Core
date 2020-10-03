import React from 'react';
import Timer from '../Timer/Timer.jsx';
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
					<Timer/>
				</Col>
			</div>
		);
	}
}