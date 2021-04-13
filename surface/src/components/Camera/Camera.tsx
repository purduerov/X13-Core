import * as React from 'react';
import CameraFrame from './CameraFrame';
import cameras from './camera.json';
import './Camera.scss';

const Camera: React.FC = () => {
	const [active, setActive] = React.useState(0);

	return(
		<div className='grid-container'>
			<div className='main-row'>
				<CameraFrame camera={cameras[active]} handleClick={(_) => {}} />
			</div>
			<div className='camera-row'>
				{cameras.map((camera, idx) => {
					if (idx != active)
						return (<CameraFrame key={idx} index={idx} camera={camera} secondary handleClick={setActive}/>);
				})}
			</div>
		</div>
	)
}

export default Camera;