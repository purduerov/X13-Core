import * as React from 'react';
import './Toggle.scss';
import test from './configs/test.json';
import Toggle from '../Toggle/Toggle';

const Profiles: React.FC = () => {

    const [selected, setSelected] = React.useState([false])

    return(
        <div>
            <Toggle name={test.name} callback={() => selected[0] = !selected[0]} toggled={selected[0]}/>
        </div>
    )
}

export default Profiles;