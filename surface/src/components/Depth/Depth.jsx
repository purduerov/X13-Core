import React from 'react';
import {Container, Col, Row} from 'react-bootstrap';
import attachDepthNode from './attachDepthNode.js';

export default class Depth extends React.Component {
	constructor(props) {
		super(props);

		this.state = {depth: 0};
        this.updateDepth = this.updateDepth.bind(this);
        attachDepthNode(this.updateDepth);
	}

    updateDepth(val){
        this.setState({depth: val});
    }


	render() {
		return (
			<Container>
                Depth: {this.state.depth}
            </Container>
		);
	}
}
