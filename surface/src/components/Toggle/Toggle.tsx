import * as React from 'react';
import './Toggle.scss';

interface Props {
    name: string
    toggled: boolean
    callback(): void
}

const Toggle: React.FC<Props> = (props) => {

    return(
        <button onClick={props.callback} className={`toggle-${props.toggled}`}>{props.name}</button>
    )
}

export default Toggle;