/* eslint-env browser */
import React from 'react';
import CameraFrame from './CameraFrame';
import cameras from './camera.json';
import './Camera.scss';

interface State{
	activeCamera: number
}

export default class Camera extends React.Component<{}, State> {
	constructor(props) {
		super(props);

		this.state = {
			activeCamera: 0,
		};

		this.handleClick = this.handleClick.bind(this);
		this.handleKeyDown = this.handleKeyDown.bind(this);
	}

	componentWillMount() {
		document.addEventListener('keydown', this.handleKeyDown);
	}

	componentWillUnmount() {
		document.removeEventListener('keydown', this.handleKeyDown);
	}

	handleKeyDown({ key }) {
		key = parseInt(key);
		if ([1,2,3,4].includes(key)) {
			this.setState({
				activeCamera: key - 1
			});
		}
	}

	handleClick(idx) {
		this.setState({
			activeCamera: idx - 1
		});
	}
	render() {
		return(
			<div className='grid-container'>
				<div className='main-row'>
					<CameraFrame type='main' handleClick={this.handleClick} camera={cameras[this.state.activeCamera]} />
				</div>
				<div className='camera-row'>
					{cameras.map((camera, idx) => {
						if (idx !== this.state.activeCamera)
							return (<CameraFrame key={idx} index={idx} camera={camera} type='secondary' handleClick={this.handleClick}/>);
					})}
				</div>
			</div>
		);
	}

}
