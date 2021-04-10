import * as React from 'react';
import {LogItem} from './LogItem';
import {ipcRenderer} from 'electron';
import './Log.scss';
import * as channels from './channels';

interface State{
    items: Array<LogItem>
}

export default class Log extends React.Component<{}, State> {
    constructor(props){
        super(props);

        this.state = {items: []};
    }
    componentDidMount(){
        ipcRenderer.send('logger', 'ready');

        channels.default.map(channel => {
            ipcRenderer.on(channel, (e, data: LogItem) => {
                this.addItem(data);
            });
        });
    }

    addItem(item: LogItem){
        this.setState({items: [...this.state.items, item]});
    }

	render() {
		return (
			<ol>
                {this.state.items.map((item, index) => {
                    return <li key={index}>{`${item.timestamp ? item.timestamp : ''} (${item.process}): ${item.text}`}</li>
                })}
            </ol>
		);
	}
}
