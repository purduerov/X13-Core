import * as React from 'react';
import './Switch.scss';

const Switch: React.FC = () => {

    return(
        <div className='switch-container'>
            <input type='checkbox' className='switch'/>
        </div>
        
    )
}

export default Switch;