import React from 'react';
import {Container} from 'react-bootstrap';
import ThrusterCircle from '../ThrusterCircle/ThrusterCircle.jsx';
import thrusterListen from '../ThrusterCircle/thrusterListen.js';

const INIT_THRUST = 127;

const T_OFF = 50;
const L_OFF = 140;

const HL = -110 + L_OFF;
const HR = 60 + L_OFF;
const VL = -80 + L_OFF;
const VR = 30 + L_OFF;
const HBT = 205 + T_OFF;
const VBT = 125 + T_OFF;
const HFT = -40 + T_OFF;
const VFT = 40 + T_OFF;


export default class ThrusterInfo extends React.Component {
	constructor(props) {
        super(props);

        this.state = {thrust: [INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST, INIT_THRUST]};

        this.updateThrust = this.updateThrust.bind(this);
		thrusterListen(this.updateThrust);
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
			<Container>
                <ThrusterCircle thrust={this.state.thrust[0]} name='HFL' top={HFT} left={HL}/>
                <ThrusterCircle thrust={this.state.thrust[1]} name='HFR' top={HFT} left={HR}/>
                <ThrusterCircle thrust={this.state.thrust[2]} name='HBR' top={HBT} left={HR}/>
                <ThrusterCircle thrust={this.state.thrust[3]} name='HBL' top={HBT} left={HL}/>
                <ThrusterCircle thrust={this.state.thrust[4]} name='VFL' top={VFT} left={VL}/>
                <ThrusterCircle thrust={this.state.thrust[5]} name='VFR' top={VFT} left={VR}/>
                <ThrusterCircle thrust={this.state.thrust[6]} name='VBR' top={VBT} left={VR}/>
                <ThrusterCircle thrust={this.state.thrust[7]} name='VBL' top={VBT} left={VL}/>
			</Container>
		);
	}
}
