import * as React from 'react';
import CameraInterface from './CameraInterface';
import './Camera.scss';

interface Props{
	handleClick(number): void
	secondary?: boolean
	index?: number
	camera: CameraInterface
}

const defaultProps: Props = {
	handleClick: (_) => {},
	secondary: false,
	camera: {
		feed: '',
		placeholder: '',
		name: ''
	}
}

const CameraFrame: React.FC<Props> = (props) => {
	const [src, setSrc] = React.useState(props.camera.feed);
	React.useEffect(() => {
		setSrc(props.camera.feed);
	}, [props.camera])

	return(
		<img src={src}
			className={props.secondary ? 'frame' : 'main-frame'}
			alt="Image not found"
			onError={() => setSrc(props.camera.placeholder)}
			onClick={() => props.handleClick(props.index)}
		/>
	)
}

CameraFrame.defaultProps = defaultProps;

export default CameraFrame;