import { ipcRenderer } from 'electron';
import * as React from 'react';
import './Mosaic.scss';

const Mosaic: React.FC = () => {
    const [counter, setCounter] = React.useState(0);

    return(
        <div className='servo-container'>
            <div className='servo-title'>Mosaic Photo {counter}/5</div>
            <button
                className='mosaic-btn'
                onClick = {(val) => {
                    setCounter(counter + 1);
                    if(counter > 4) setCounter(0);
                    ipcRenderer.send('mosaic_send', counter);
                }}>
                Save Frame
            </button>
        </div>
    )
}

export default Mosaic;