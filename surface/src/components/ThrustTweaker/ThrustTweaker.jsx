import React, {useState, useEffect} from 'react';
import './ThrustTweaker.css';
import {connect, send} from '../../tools/ipc.js';

export default function ThrustTweaker(){
    const [constants, setConstants] = useState([4.0, 4.0, 4.0, 1.0, 1.0, 1.0]);
    const [globals, setGlobals] = useState([4.0, 1.0]);

    useEffect(() => {
        connect(11001);
    }, []);    

    function handleConstants(e, id){
        let c = [...constants];
        c[id] = e.target.value;
        console.log(c);
        console.log(constants);
        setConstants(c);
        send(constants);
    }

    function handleTranslation(e){
        let c = [...constants];
        for(let i = 0; i < 3; i++){
            c[i] = e.target.value;
        }
        setConstants(c);
        setGlobals([e.target.value, globals[1]]);
        send(constants);
    }

    function handleRotation(e){
        let c = [...constants];
        for(let i = 3; i < 6; i++){
            c[i] = e.target.value;
        }
        setConstants(c);
        setGlobals([globals[0], e.target.value]);
        send(constants);
    }

    return(
        <div className="thruster-container">
            <b className="thruster-title">Thruster Power Tweaks</b>
            <label><b>Translation</b></label>
            <input type="range" value={globals[0]} min={0.0} max={10.0} step={0.1} onChange={(e) => {handleTranslation(e)}} />
            <label>X Translation: {constants[0]}</label>
            <input type="range" value={constants[0]} min={0.0} max={10.0} step={0.1} onChange={(e) => {handleConstants(e, 0)}} />
            <label>Y Translation: {constants[1]}</label>
            <input type="range" value={constants[1]} min={0.0} max={10.0} step={0.1} onChange={(e) => {handleConstants(e, 1)}} />
            <label>Z Translation: {constants[2]}</label>
            <input type="range" value={constants[2]} min={0.0} max={10.0} step={0.1} onChange={(e) => {handleConstants(e, 2)}} />
            <label><b>Rotation</b></label>
            <input type="range" value={globals[1]} min={0.0} max={2.0} step={0.1} onChange={(e) => {handleRotation(e)}} />
            <label>X Rotation: {constants[3]}</label>
            <input type="range" value={constants[3]} min={0.0} max={2.0} step={0.1} onChange={(e) => {handleConstants(e, 3)}} />
            <label>Y Rotation: {constants[4]}</label>
            <input type="range" value={constants[4]} min={0.0} max={2.0} step={0.1} onChange={(e) => {handleConstants(e, 4)}} />
            <label>Z Rotation: {constants[5]}</label>
            <input type="range" value={constants[5]} min={0.0} max={2.0} step={0.1} onChange={(e) => {handleConstants(e, 5)}} />
        </div>
    );
}
