import React, { Component } from 'react';
import {Container, Row, Col} from 'react-bootstrap';
import PropTypes from 'prop-types';
import './LinearGauge.css';

export default class LinearGauge extends React.Component {
    render() {
      let showInd = this.props.value != 0;
      let shiftH = this.props.height / 6;
      let shiftW = this.props.width / 3;
      let pointerH = this.props.gauge_width / 2;
      let pointerW = (this.props.gauge_width * 3) / 4;
      let pointerStr = "0,-" + pointerH + " 0," + pointerH + " " +  pointerW + ",0";
      console.log(pointerStr);
        return (
          <Container>
          <Row>
          <svg width={this.props.width} height={this.props.height}>
          <g>
            <svg width={this.props.gauge_width} height={this.props.gauge_height} x={"" + shiftW} y={"" + shiftH}>
                    <rect width={this.props.gauge_width} height={this.props.gauge_height} fill="#39B4CC"></rect>
                    <rect width={this.props.gauge_width} height={this.props.gauge_height-this.props.value} fill="#A6A6A6"></rect>
            </svg>
            </g>
            { (()=> {
              if (showInd) {
                return (<g transform={"translate(0,"+((this.props.gauge_height + shiftH) - this.props.value) + ")"}>
                  <polygon points={pointerStr} fill="#807E7E"/>
                </g>)
          }})()};
            </svg>
            <span className='val'>{this.props.value + this.props.value_unit}</span>
            </Row>
            <Row>
            <span className='name'>{this.props.name}</span>
            </Row>
            </Container>
        )
    }
}

LinearGauge.defaultProps = {
  value: 0,
  value_unit: "%",
  name: "NaN",
  height: 150,
  width: 75,
  gauge_height: 100,
  gauge_width: 20
}
