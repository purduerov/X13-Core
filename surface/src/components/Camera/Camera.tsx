import * as React from 'react';
import CameraFrame from './CameraFrame';
import cameras from './camera.json';
import './Camera.scss';

const Camera: React.FC = () => {
	const [active, setActive] = React.useState(0);
	const [rotate, setRotate] = React.useState(0);

	return(
		<div className='grid-container'>
			<div className='main-row'>
				<CameraFrame camera={cameras[active]} rotate={rotate} handleClick={(_) => {}} />
			</div>
			<div className='camera-row'>
				{cameras.map((camera, idx) => {
					if (idx != active)
						return (<CameraFrame key={idx} index={idx} rotate={0} camera={camera} secondary handleClick={(idx) => {
							setActive(idx);
							setRotate(cameras[idx].angle);
						}}/>);
				})}
				<button onClick={() => {
					if(rotate == 360) setRotate(0);
					else setRotate(rotate + 90);
				}}>Rotate Main</button>
			</div>
		</div>
	)
}

export default Camera;