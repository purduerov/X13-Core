import { ipcRenderer } from 'electron';
import * as React from 'react';
import ThrusterCircle from '../ThrusterCircle/ThrusterCircle';
import './ThrusterInfo.scss';

const INIT_THRUST = 127;

const ThrusterInfo: React.FC = () => {
	const [thrust, setThrust] = React.useState<Array<number>>(Array(8).fill(INIT_THRUST));

	ipcRenderer.on('thrusters', (e, data: Array<number>) => {
		setThrust(data)
	});

	return (
		<div className="thruster-container">
			<ThrusterCircle className="thruster-left" thrust={thrust[4]} name='HFL'/>
			<ThrusterCircle className="thruster-right" thrust={thrust[7]} name='HFR'/>
			<ThrusterCircle className="thruster-right" thrust={thrust[0]} name='VFL'/>
			<ThrusterCircle className="thruster-left" thrust={thrust[3]} name='VFR'/>
			<ThrusterCircle className="thruster-right" thrust={thrust[1]} name='VBL'/>
			<ThrusterCircle className="thruster-left" thrust={thrust[2]} name='VBR'/>
			<ThrusterCircle className="thruster-left" thrust={thrust[5]} name='HBL'/>
			<ThrusterCircle className="thruster-right" thrust={thrust[6]} name='HBR'/>        
		</div>
	)
}

export default ThrusterInfo;
