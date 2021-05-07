import * as React from 'react';
import './Switch.scss';

interface Props {
    checked: boolean
    callback(): void
}

const Switch: React.FC<Props> = (props) => {

    return(
        <div className='switch-container'>
            <input type='checkbox' className='switch' checked={props.checked} onChange={props.callback}/>
        </div>
        
    )
}

export default Switch;