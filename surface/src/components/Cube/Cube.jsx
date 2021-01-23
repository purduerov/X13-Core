import React from 'react';
import {Container, Button} from 'react-bootstrap';
import * as t from 'three';
import imuListen from './imuListen.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import {ipcRenderer} from 'electron';

export default class Cube extends React.Component {
	constructor(props) {
        super(props);
        this.state = {gamepad: {RSY: -0.8}, imu: [0, 0, 0], offset: [Math.PI / 2, 0, -(Math.PI / 2)]};
        this.animate = this.animate.bind(this);
		this.process = null;

		this.monitor = this.monitor.bind(this);
        this.updateImu = this.updateImu.bind(this);
		imuListen(this.updateImu, this.monitor);
		this.handleCalibrate = this.handleCalibrate.bind(this);

        this.rov = false;

		this.loadModel = this.loadModel.bind(this);

		ipcRenderer.on('kill', (event, args) => {
			console.log('Killing...');
			this.kill();
		});
    }

	monitor(process){
		this.process = process;
	}

	kill(){
		if(this.process){
			this.process.kill('SIGKILL');
		}
	}

    modifyValues(vals){
		const list = this.state.imu.map((t, idx) => vals[idx]);

		return list;
	}

    updateImu(data){
		this.setState({imu: this.modifyValues(data)});
	}

    componentDidMount(){
        const width = this.mount.clientWidth;
        const height = this.mount.clientHeight;

        const scene = new t.Scene();
        const camera = new t.PerspectiveCamera(
          75,
          width / height,
          0.1,
          1000
        );

		const light = new t.RectAreaLight(0xffffff, 1.4, 100, 100);
	    light.position.set(1, 1, 10);
	    light.lookAt(1, 1, 3);
	    scene.add(light)

        const renderer = new t.WebGLRenderer({antialias: true, alpha: true});

		const material_horizon = new t.LineBasicMaterial({color: 0xFFFFFF});
		const material_rov = new t.LineDashedMaterial({
			color: 0xFFFFFF,
			linewidth: 1,
			scale: 1,
			dashSize: 0.05,
			gapSize: 0.05,
		});
		const geometry_rov = new t.BufferGeometry().setFromPoints([new t.Vector3(-0.5, 0, 0), new t.Vector3(0.5, 0, 0)]);
		const line_rov = new t.Line(geometry_rov, material_rov);
		const geometry_horizon = new t.BufferGeometry().setFromPoints([new t.Vector3(-1, 0, 0), new t.Vector3(1, 0, 0)]);
		const line_horizon = new t.Line(geometry_horizon, material_horizon);
		line_rov.computeLineDistances();
		scene.add(line_rov);
		scene.add(line_horizon)

		this.loadModel(this);

        camera.position.z = 0.49;
        camera.position.y = 0.3;
		camera.rotation.x = -(1/8 * Math.PI)

        renderer.setClearColor('#000000', 0);
        renderer.setSize(width, height);

        this.scene = scene;
        this.camera = camera;
        this.renderer = renderer;

        this.mount.appendChild(this.renderer.domElement);

        requestAnimationFrame(this.animate);
    }

	handleCalibrate(){
		let newX = (this.state.imu[2] / 180) * Math.PI + Math.PI / 1.5;
		let newZ = Math.PI / 2 - (this.state.imu[0] / 180) * Math.PI;


		console.log(this.state.offset);
		this.setState({offset: [newX, 0, newZ]});
		console.log(this.state.offset);
		console.log(this.state.imu);
	}

	loadModel(context){
		const loader = new GLTFLoader();

		loader.load('../src/components/Cube/ROV.glb', function(gltf){
			context.rov = gltf.scene;
			context.scene.add(context.rov);
        }, undefined, function (error) {
        	console.error(error);
        });
	}

    animate() {
		if(this.rov){
			this.rov.rotation.x = (this.state.imu[0] / 180) * Math.PI - this.state.offset[0];
	        this.rov.rotation.y = (this.state.imu[2] / 180) * Math.PI - this.state.offset[2]
	        this.rov.rotation.z = Math.PI / 2;
		}

        this.renderScene();
        this.frameId = window.requestAnimationFrame(this.animate);
    }

    renderScene() {
        this.renderer.render(this.scene, this.camera);
    }

	render() {
		return (
			<Container style={{ width: '100%', height: '200px', position: 'relative', top: '500px'}} ref={(mount) => { this.mount = mount }}>
				<Button onClick={this.handleCalibrate}>Calibrate</Button>
			</Container>
		);
	}
}
