import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Col } from 'react-bootstrap';

export default class CameraFrame extends Component {
	constructor(props) {
		super(props);
				
		this.state={
			img: this.props.camera.highres,
			load_img: this.props.camera.placeholder,
			loaded: false
		};
	}	
	displayLoadingImage() {
		this.setState({loaded: true});	
	}
	render() {
		
		const { loaded } = this.state;
		const frameStyle = !loaded ? { width: '100%', display: "none"} : {width: '100%'}
		const placeholderStyle = {width:'100%'}
		const loadImg = <img src={this.state.load_img} style={placeholderStyle}/>
		// Note: camImg will not update each frame.
		const camImg = <img src={this.props.camera.highres} style={frameStyle} alt="Image not found" 
					ref={img => this.img = img} onError={() => this.img.src = this.props.camera.placeholder} 
					onLoad={this.displayLoadingImage.bind(this)}/>
				
		if (this.props.res == 'high') {
			// must update
			return (
				
				<div>

					{(!loaded) && <img src={this.state.load_img} style={placeholderStyle}/>}
					<img src={this.props.camera.highres} style={frameStyle} alt="Image not found" 
						ref={img => this.img = img} onError={() => this.img.src = this.props.camera.placeholder} 
						onLoad={this.displayLoadingImage.bind(this)}/>
							
				</div>
			);
		} else {
			return (
				<div onClick={this.props.handleClick(this.props.idx)}>
				{(!loaded) ? <img src={this.state.load_img} style={placeholderStyle}/> : {camImg}}
					

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
		placeholder: PropTypes.string.isRequired
	})
};
