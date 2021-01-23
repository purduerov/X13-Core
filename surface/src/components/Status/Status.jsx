import React from 'react';
import './Status.css';

export default class Status extends React.Component {
	constructor(props) {
		super(props);

        this.state = {module: this.props.module, status: this.props.status};
        this.style = {backgroundColor: '#39B4CC'};

        this.updateStatus();
	}

    updateStatus(){
		this.style = this.state.status();
    }

	render() {
		return (
            <span>
    	        <span className="colored-circle" style={this.style}/>
                <span>{this.state.module}</span>
            </span>
		);
	}
}
