import * as React from 'react';
import CameraInterface from './CameraInterface';
import './Camera.scss';

interface Props{
	handleClick(number): void
	secondary?: boolean
	index?: number
	rotate: number
	camera: CameraInterface
}

const defaultProps: Props = {
	handleClick: (_) => {},
	secondary: false,
	rotate: 0,
	camera: {
		feed: '',
		placeholder: '',
		name: '',
		angle: 0
	}
}

const CameraFrame: React.FC<Props> = (props) => {
	const [src, setSrc] = React.useState(props.camera.feed);
	React.useEffect(() => {
		setSrc(props.camera.feed);
	}, [props.camera])

	return(
		<div 
			style={{
				backgroundImage: `URL(${src})`, 
				transform: `rotate(${props.rotate}deg) ${props.rotate == 90 || props.rotate == 270 ? `translateX(${(180 - props.rotate) / 90 * 170}px)` : ''}`
			}}
			className={props.secondary ? 'frame' : `main-frame ${props.rotate == 90 || props.rotate == 270 ? 'main-frame-vert' : ''}`}
			onError={() => setSrc(props.camera.placeholder)}
			onClick={() => props.handleClick(props.index)}
		/>
	)
}

CameraFrame.defaultProps = defaultProps;

export default CameraFrame;