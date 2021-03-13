import React, {useState} from 'react';
import './ThrustTweaker.css';
import {connect, send} from '../../tools/ipc.js';

export default function ThrustTweaker(){
    const [constants, setConstants] = useState([4.0, 4.0, 4.0, 1.0, 1.0, 1.0]);
    const [globals, setGlobals] = useState([4.0, 1.0]);

    connect(11001);

    function handleConstants(e, id){
        let c = constants;
        c[id] = e.target.value;
        send(c);
        return c;
    }

    function handleTranslation(e){
        let c = constants;
        for(let i = 0; i < 3; i++){
            c[i] = e.target.value;
        }
        setConstants(c);
        setGlobals([e.target.value, globals[1]]);
        send(constants);
    }

    function handleRotation(e){
        let c = constants;
        for(let i = 3; i < 6; i++){
            c[i] = e.target.value;
        }
        setConstants(c);
        setGlobals([globals[0], e.target.value]);
        send(constants);
    }

    return(
        <div className="thruster-container">
            <label><b>Translation</b></label>
            <input type="range" value={globals[0]} min={0.0} max={10.0} step={0.1} onChange={(e) => {handleTranslation(e)}} />
            <label>X Translation</label>
            <input type="range" value={constants[0]} min={0.0} max={10.0} step={0.1} onChange={(e) => {setConstants(handleConstants(e, 0))}} />
            <label>Y Translation</label>
            <input type="range" value={constants[1]} min={0.0} max={10.0} step={0.1} onChange={(e) => {setConstants(handleConstants(e, 1))}} />
            <label>Z Translation</label>
            <input type="range" value={constants[2]} min={0.0} max={10.0} step={0.1} onChange={(e) => {setConstants(handleConstants(e, 2))}} />
            <label><b>Rotation</b></label>
            <input type="range" value={globals[1]} min={0.0} max={2.0} step={0.1} onChange={(e) => {handleRotation(e)}} />
            <label>X Rotation</label>
            <input type="range" value={constants[3]} min={0.0} max={2.0} step={0.1} onChange={(e) => {setConstants(handleConstants(e, 3))}} />
            <label>Y Rotation</label>
            <input type="range" value={constants[4]} min={0.0} max={2.0} step={0.1} onChange={(e) => {setConstants(handleConstants(e, 4))}} />
            <label>Z Rotation</label>
            <input type="range" value={constants[5]} min={0.0} max={2.0} step={0.1} onChange={(e) => {setConstants(handleConstants(e, 5))}} />
        </div>
    );
}
