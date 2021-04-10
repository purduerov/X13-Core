import { ipcRenderer } from 'electron';
import * as React from 'react';
import ThrusterCircle from '../ThrusterCircle/ThrusterCircle';
import './ThrusterInfo.scss';

const INIT_THRUST = 127;

interface State{
    thrust: Array<number>
}

export default class ThrusterInfo extends React.Component<{}, State> {
	constructor(props: {}) {
        super(props);

        this.state = {thrust: [INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST]};
    }

	componentDidMount(){
		ipcRenderer.on('thrusters', (e, data: Array<number>) => {
			this.setState({thrust: data})
		});
	}

	render() {
		return (
			<div className="thruster-container">
                <ThrusterCircle className="thruster-left" thrust={this.state.thrust[4]} name='HFL'/>
                <ThrusterCircle className="thruster-right" thrust={this.state.thrust[7]} name='HFR'/>
				<ThrusterCircle className="thruster-right" thrust={this.state.thrust[0]} name='VFL'/>
				<ThrusterCircle className="thruster-left" thrust={this.state.thrust[3]} name='VFR'/>
				<ThrusterCircle className="thruster-right" thrust={this.state.thrust[1]} name='VBL'/>
				<ThrusterCircle className="thruster-left" thrust={this.state.thrust[2]} name='VBR'/>
				<ThrusterCircle className="thruster-left" thrust={this.state.thrust[5]} name='HBL'/>
                <ThrusterCircle className="thruster-right" thrust={this.state.thrust[6]} name='HBR'/>        
			</div>
		);
	}
}
