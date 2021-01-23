import React from 'react';
import './Status.css';

export default class Status extends React.Component {
	constructor(props) {
		super(props);

        this.state = {status: this.props.status, module: this.props.module};
        this.style = {backgroundColor: '#39B4CC'};

        this.updateStatus();
	}

    updateStatus(){
        if(this.state.status){
            this.style = {backgroundColor: '#00FF00'};
        }else{
            this.style = {backgroundColor: '#FF0000'};
        }
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
