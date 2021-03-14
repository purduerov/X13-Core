import React from 'react';
import PropTypes from 'prop-types';
import { Col, Container } from 'react-bootstrap';

export default class CameraFrame extends React.Component {
	constructor(props) {
		super(props);
		console.log(this.props.camera);
		this.state={
			img: this.props.camera.camFeed,
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
		const camImg = <img src={this.props.camera.camFeed}
							style={frameStyle} alt="Image not found"
							ref={img => this.img = img}
							onError={() => this.img.src = this.props.camera.placeholder}
							onLoad={this.displayLoadingImage.bind(this)}/>

		if (this.props.type == 'viewport') {
			// Main camera-- has no onClick()
			// must update

			return (

				<div>
					{(!loaded) && <img src={this.state.load_img} style={placeholderStyle}/>}
					<img src={this.props.camera.camFeed}
						 style={frameStyle}
						 alt="Image not found"
						 ref={img => this.img = img}
						 onError={() => this.img.src = this.props.camera.placeholder}
						 onLoad={this.displayLoadingImage.bind(this)}/>
				</div>
			);
		} else {
			// Type is selection menu, so it must be clickable.
			return (
				<div onClick={this.props.handleClick(this.props.idx)}>
					{(!loaded) ? <img src={this.state.img} style={placeholderStyle}/> : {camImg}}
				</div>
			);
		}
	}
}

CameraFrame.propTypes = {
	handleClick: PropTypes.func,
	type: PropTypes.string.isRequired,
	idx: PropTypes.number,
	camera: PropTypes.shape({
		camFeed: PropTypes.string.isRequired,
		placeholder: PropTypes.string.isRequired
	})
};
