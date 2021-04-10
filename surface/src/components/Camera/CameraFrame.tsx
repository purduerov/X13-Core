import React from 'react';
import CameraInterface from './CameraInterface';
import './Camera.scss';

interface Props{
	handleClick(number): void
	type: 'main' | 'secondary'
	index?: number
	camera: CameraInterface
}

interface State{
	img: string
	loadImg: string
	loaded: boolean
}

export default class CameraFrame extends React.Component<Props, State> {
	constructor(props) {
		super(props);

		this.state={
			img: this.props.camera.feed,
			loadImg: this.props.camera.placeholder,
			loaded: false
		};

		this.imageError = this.imageError.bind(this);
		this.imageLoad = this.imageLoad.bind(this);
	}

	imageError(){
		this.setState({img: this.props.camera.placeholder});
	}

	imageLoad(){
		this.setState({loaded: true});
	}

	render() {
		return (
			<img src={this.state.img}
				className={this.props.type == 'main' ? 'main-frame' : 'frame'}
				alt="Image not found"
				onError={this.imageError}
				onLoad={this.imageLoad}
				onClick={this.props.type == 'secondary' ? () => this.props.handleClick(this.props.index) : () => {}}/>
		);
	}
}