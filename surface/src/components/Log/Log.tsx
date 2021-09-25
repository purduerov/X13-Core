import * as React from 'react';
import {LogItem} from './LogItem';
import {ipcRenderer} from 'electron';
import './Log.scss';
import * as channels from './channels';


const Log: React.FC = () => {
    const [items, setItems] = React.useState<Array<LogItem>>([]);

    React.useEffect(() => {
        ipcRenderer.send('logger', 'ready');

        channels.default.map(channel => {
            ipcRenderer.on(channel, (e, data: LogItem) => {
                setItems(old => [...old, data]);
            });
        });
    }, [])

    return(
        <ol>
            {items.map((item, index) => {
                return <li key={index}>
                    {`${item.timestamp ? item.timestamp : ''} (${item.process})`}: <span style={{color: item.color}}>{item.text}</span>
                </li>
            })}
        </ol>
    )
}

export default Log;

