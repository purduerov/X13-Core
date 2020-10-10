import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Col } from 'react-bootstrap';

export default class CameraFrame extends Component {
	render() {
		if (this.props.res == 'high') {
			return (
				<div>
					<img src={this.props.camera.lowres} style={{height: '100%'}}/>
				</div>
			);
		} else {
			return (
				<div onClick={this.props.handleClick(this.props.idx)}>
					<img src={this.props.camera.lowres} style={{width: '100%'}}/>
				</div>
			);
		}
	}
}

CameraFrame.propTypes = {
	handleClick: PropTypes.func,
	res: PropTypes.string.isRequired,
	idx: PropTypes.number,
	camera: PropTypes.shape({
		highres: PropTypes.string.isRequired,
		lowres: PropTypes.string.isRequired
	})
};
