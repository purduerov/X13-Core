import React from 'react';
import Timer from '../Timer/Timer.jsx';
import './Titlebar.css';

export default class Titlebar extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className='title'>
				<div className='col col-align'>
					Purdue ROV Main Screen
				</div>

				<div className='col'>
					<Timer></Timer>
				</div>
			</div>
		);
	}
}