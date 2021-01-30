import React from 'react';
import {Container, Button} from 'react-bootstrap';
import * as t from 'three';
import imuListen from './imuListen.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import {ipcRenderer} from 'electron';
import {monitor, kill} from './../../tools/procMonitor.js';

export default class Cube extends React.Component {
	constructor(props) {
        super(props);
        this.state = {gamepad: {RSY: -0.8}, imu: [0, 0, 0], offset: [Math.PI / 2, 0, 0]};
        this.animate = this.animate.bind(this);

		this.monitor = monitor.bind(this);
		this.kill = kill.bind(this);

		this.handleCalibrate = this.handleCalibrate.bind(this);
        this.updateImu = this.updateImu.bind(this);
		this.loadModel = this.loadModel.bind(this);
		imuListen(this.updateImu, this.monitor);

        this.rov = false;
		this.line_rov = new t.Line(new t.BufferGeometry().setFromPoints([new t.Vector3(-0.5, 0, 0), new t.Vector3(0.5, 0, 0)]), new t.LineDashedMaterial({
			color: 0xFFFFFF,
			linewidth: 1,
			scale: 1,
			dashSize: 0.05,
			gapSize: 0.05,
		}));

		ipcRenderer.on('kill', (event, args) => {
			console.log('Killing...');
			this.kill();
		});
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
		const geometry_horizon = new t.BufferGeometry().setFromPoints([new t.Vector3(-1, 0, 0), new t.Vector3(1, 0, 0)]);
		const line_horizon = new t.Line(geometry_horizon, material_horizon);

		const cm_1 = new t.Mesh(new t.PlaneGeometry(0.5, 0.25), new t.MeshBasicMaterial({color: 0xbafffc, side: t.DoubleSide}));
		const cm_2 = new t.Mesh(new t.PlaneGeometry(0.5, 0.25), new t.MeshBasicMaterial({color: 0xb5b5b5, side: t.DoubleSide}));
		const cm_3 = new t.Mesh(new t.PlaneGeometry(0.5, 0.25), new t.MeshBasicMaterial({color: 0xb5b5b5, side: t.DoubleSide}));
		scene.add(cm_1);
		scene.add(cm_2);
		scene.add(cm_3);
		cm_1.position.z = -0.5;
		cm_2.position.x = 0.5;
		cm_2.rotation.y = Math.PI/2;
		cm_3.position.x = -0.5;
		cm_3.rotation.y = Math.PI/2;


		this.line_rov.computeLineDistances();
		scene.add(this.line_rov);
		scene.add(line_horizon);

		this.loadModel(this);

        camera.position.z = 0.55;
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
		let newX = (this.state.imu[0] / 180) * Math.PI + Math.PI / 2;
		let newY = -(this.state.imu[2] / 180) * Math.PI;

		this.setState({offset: [newX, newY, 0]});
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
			this.rov.rotation.y = (this.state.imu[2] / 180) * Math.PI - this.state.offset[1]
	        this.rov.rotation.z = Math.PI / 2;
			this.line_rov.rotation.z = -this.rov.rotation.y;
		}

        this.renderScene();
        window.requestAnimationFrame(this.animate);
    }

    renderScene() {
        this.renderer.render(this.scene, this.camera);
    }

	render() {
		return (
			<Container style={{ width: '100%', height: '90%'}} ref={(mount) => { this.mount = mount }}>
				<Button onClick={this.handleCalibrate}>Calibrate</Button>
			</Container>
		);
	}
}
