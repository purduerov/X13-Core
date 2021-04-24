import { ipcRenderer } from 'electron';
import * as React from 'react';
import * as three from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader';

interface T{
    scene: three.Scene
    camera: three.PerspectiveCamera
    renderer: three.WebGL1Renderer
    geometry: three.BoxGeometry
    material: three.MeshBasicMaterial
}

let orientation = [0, 0, 0]
let rov;

const loadModel = async (s: T) => {
    const loader = new GLTFLoader();

    loader.load('./ROV.glb', (gltf) => {
        rov = gltf.scene
        s.scene.add(rov);
        rov.rotation.z = Math.PI / 2;
    }, 
    undefined,
    (e) => {
        console.log(e);
    });
}

const setup = (element: Element): T => {
    const width = element.clientWidth;
    const height = element.clientHeight;
    let r: T = {
        scene: new three.Scene(),
        camera: new three.PerspectiveCamera(80, width / height, 0.1, 1000),
        renderer: new three.WebGL1Renderer({antialias: true, alpha: true}),
        geometry: new three.BoxGeometry(),
        material: new three.MeshBasicMaterial({color: 0x00ff00}),
    }

    return r
}

const animate = (s: T) => {
    s.renderer.render(s.scene, s.camera);
    if(rov){
        rov.rotation.x = ((orientation[0] - 90) / 180) * Math.PI;
        rov.rotation.y = ((orientation[2] - 180) / 180) * Math.PI;
    }

    requestAnimationFrame(() => animate(s));
};

const IMU: React.FC = () => {

    const ref = React.useRef<any>(null);
    const [offsets, setOffsets] = React.useState<Array<number>>([0.0, 0.0, 0.0]);

    ipcRenderer.on('imu', (e, data) => {
        orientation = data;
    })

    React.useEffect(() => {
        const s = setup(ref.current);
    
        s.renderer.setSize(ref.current.clientWidth, ref.current.clientHeight);
        
        s.camera.position.z = 0.65;
		s.camera.position.y = 0.3;
		s.camera.rotation.x = -(1/8 * Math.PI)

        const light = new three.RectAreaLight(0xffffff, 1.4, 100, 100);
		light.position.set(1, 1, 10);
		light.lookAt(1, 1, 3);
		s.scene.add(light);

        loadModel(s).then(() => {
            requestAnimationFrame(() => animate(s));
        })

        ref.current.appendChild(s.renderer.domElement);    
    }, [])

    return(
        <div>
            <button onClick={() => {

                }}>
                Calibrate (Not Available)
            </button>
            <div style={{width: '100%', height: '100%'}} ref={ref}></div>
        </div>     
    )
}

export default IMU