import React from 'react';
import './Status.css';

export default class Status extends React.Component {
	constructor(props) {
		super(props);

        this.state = {module: this.props.module};
		console.log(this.props.status);
	}

	render() {
		return (
            <span>
    	        <span className="colored-circle" style={this.props.status}/>
                <span>{this.state.module}</span>
            </span>
		);
	}
}
