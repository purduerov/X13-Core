import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Col } from 'react-bootstrap';

export default class CameraFrame extends Component {
	constructor(props) {
		super(props);
		
		this.state={img: this.props.camera.highres};
	}	
	getBackupImage() {
			
	}
	render() {
		if (this.props.res == 'high') {
			// must update
			this.state.img=this.props.camera.highres;
			return (
				
				<div>
					
					<img src={this.state.img} style={{width: '100%'}} alt="Image not found" ref={img => this.img = img} onError={() => this.img.src = this.props.camera.lowres}/>
				</div>
			);
		} else {
			return (
				<div onClick={this.props.handleClick(this.props.idx)}>
					<img src={this.state.img} style={{width: '100%'}} ref={img => this.img = img} onError={() => this.img.src = this.props.camera.lowres}/>
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
