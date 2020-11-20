import React from 'react';
import {Container} from 'react-bootstrap';
import * as t from 'three';
import imuListen from './imuListen.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';


export default class Cube extends React.Component {
	constructor(props) {
        super(props);
        this.state = {gamepad: {RSY: -0.8}, imu: [0, 0, 0]};
        this.animate = this.animate.bind(this);

        this.updateImu = this.updateImu.bind(this);
		imuListen(this.updateImu);

        this.rov = '';
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
        const renderer = new t.WebGLRenderer({ antialias: true, alpha: true });
        const geometry = new t.BoxGeometry(3, 0.5, 2);
        const material = new t.MeshBasicMaterial({ color: '#433F81'});
        const cube = new t.Mesh(geometry, material);

        const loader = new GLTFLoader();
        loader.load('../src/components/Cube/ROV.glb', function(gltf){
            //scene.add(gltf.scene);

        }, undefined, function ( error ) {
        	console.error( error );
        } );

        camera.position.z = 3;
        camera.position.y = 0;
        scene.add(cube);
        renderer.setClearColor('#000000', 0);
        renderer.setSize(width, height);

        this.scene = scene;
        this.camera = camera;
        this.renderer = renderer;
        this.material = material;
        this.cube = cube;

        this.mount.appendChild(this.renderer.domElement);

        requestAnimationFrame(this.animate);
    }

    animate() {
        //this.cube.rotation.x += 0.01;
        //this.cube.rotation.y += 0.01;

        this.cube.rotation.x = this.state.imu[2];
        this.cube.rotation.y = 0;
        this.cube.rotation.z = this.state.imu[0];




        this.renderScene();
        this.frameId = window.requestAnimationFrame(this.animate);
    }

    renderScene() {
        this.renderer.render(this.scene, this.camera);
    }



	render() {
		return (
			<Container style={{ width: 'auto', height: '200px', position: 'relative', top: '500px'}} ref={(mount) => { this.mount = mount }}/>
		);
	}
}
