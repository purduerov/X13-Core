import React from 'react';
import {Container} from 'react-bootstrap';
import ThrusterCircle from '../ThrusterCircle/ThrusterCircle.jsx';
import thrusterListen from './thrusterListen.js';
import {ipcRenderer} from 'electron';
import {monitor, kill} from './../../tools/procMonitor.js';
import './ThrusterInfo.css';

const INIT_THRUST = 127;

export default class ThrusterInfo extends React.Component {
	constructor(props) {
        super(props);

        this.state = {thrust: [INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST]};

        this.updateThrust = this.updateThrust.bind(this);
		this.monitor = monitor.bind(this);
		this.kill = kill.bind(this);
		thrusterListen(this.updateThrust, this.monitor);

		ipcRenderer.on('kill', (event, args) => {
			console.log('Killing...');
			this.kill();
		});
    }

    modifyValues(vals){
		const list = this.state.thrust.map((t, idx) => vals[idx]);

		return list;
	}

    updateThrust(data){
		this.setState({thrust: this.modifyValues(data)});
	}

	render() {
		return (
			<div className="thruster-container">
                <ThrusterCircle className="thruster-left" thrust={this.state.thrust[4]} name='HFL'/>
                <ThrusterCircle className="thruster-right" thrust={this.state.thrust[7]} name='HFR'/>
                <ThrusterCircle className="thruster-right" thrust={this.state.thrust[6]} name='HBR'/>
                <ThrusterCircle className="thruster-left" thrust={this.state.thrust[5]} name='HBL'/>
                <ThrusterCircle className="thruster-right" thrust={this.state.thrust[0]} name='VFL'/>
                <ThrusterCircle className="thruster-left" thrust={this.state.thrust[3]} name='VFR'/>
                <ThrusterCircle className="thruster-left" thrust={this.state.thrust[2]} name='VBR'/>
                <ThrusterCircle className="thruster-right" thrust={this.state.thrust[1]} name='VBL'/>
			</div>
		);
	}
}
