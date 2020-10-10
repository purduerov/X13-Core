/* eslint-env browser */
import React from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Container } from 'react-bootstrap';

import CameraFrame from './CameraFrame.jsx';
import CameraConfig from './camera.json';

export default class Camera extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			cameras: CameraConfig,
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
		console.log(`mom ${typeof key} ${key}`);
		if ([1,2,3,4].includes(key)) {
			console.log(this);
			this.setState({
				activeCamera: key - 1
			});
		}
	}

	handleClick(idx) {
		return () => {
			this.setState({
				activeCamera: idx
			});
		};
	}
	render(props) {
		if (this.props.mode == "main_window") {
		
			return (
				<Container>
					<CameraFrame camera={this.state.cameras[this.state.activeCamera]} res="high"/>
				</Container>
			
			);
		} else if (this.props.mode == "row_box") {
			return (
				<Container>
					<Row style={{height: '100%'}}>
						{this.state.cameras.map((camera, idx) => {
							if (idx !== this.state.activeCamera)
								return <CameraFrame key={idx} idx={idx} camera={camera} res="low" handleClick={this.handleClick}/>;
						})}
					</Row>
				</Container>
			);
		} else if (this.props.mode == "column_box") {
			return (
				<Container>
					<Col style={{width: '100%'}}>
						{this.state.cameras.map((camera, idx) => {
							if (idx !== this.state.activeCamera)
								return <CameraFrame key={idx} idx={idx} camera={camera} res="low" handleClick={this.handleClick}/>;
						})}
					</Col>
				</Container>
			);
		} 
		else return (
			<p>
			Mode not selected.
			</p>
			);
	}

}
Camera.propTypes = {
	activeCamera: PropTypes.number.isRequired
};

