import React from 'react';
import {Container} from 'react-bootstrap';

export default class Console extends React.Component {
	constructor(props) {
        super(props);
    }

	render() {
		return (
			<Container className='overflow-auto'>
                {this.props.output.map((line) => <div>{line}</div>)}
			</Container>
		);
	}
}
