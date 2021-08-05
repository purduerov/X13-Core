import { ipcRenderer } from 'electron';
import * as React from 'react';
import './Mosaic.scss';

const Mosaic: React.FC = () => {
    const [counter, setCounter] = React.useState(0);

    React.useEffect(() => {
        if(counter == 4){
            ipcRenderer.send('process_frames');
        }
    }, [counter])

    return(
        <div className='servo-container'>
            <div className='servo-title'>Mosaic Photo {counter}/5</div>
            <button
                className='mosaic-btn'
                onClick = {(val) => {
                    setCounter(counter + 1);
                    if(counter > 3) setCounter(0);
                    ipcRenderer.send('take_frame', counter);
                }}>
                Save Frame
            </button>
        </div>
    )
}

export default Mosaic;