import React, { Component } from 'react';
import PropTypes from 'prop-types';

export default class LinearGauge extends React.Component {
    render() {
      let showInd = this.props.value != 0;
      let shiftH = this.props.height / 6;
      let shiftW = this.props.width / 4;
      let pointerH = this.props.gauge_width / 2;
      let pointerW = (this.props.gauge_width * 3) / 4;
      let textW = (this.props.width * 4) / 7;
      let textH = (this.props.width * 7) / 10;
      let textHN = (this.props.width * 9) / 10;
      let pointerStr = "0,-" + pointerH + " 0," + pointerH + " " +  pointerW + ",0";
      console.log(pointerStr);
        return (
          <svg width={this.props.width} height={this.props.height}>
          <g>
            <svg width={this.props.gauge_width} height={this.props.gauge_height} x={shiftW.toString()} y={shiftH.toString()}>
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
          <text x={textW} y={textH} font="15px" fill="#ffffff">{this.props.value.toString().concat(this.props.value_unit)}</text>
          <text x={textW} y={textHN} font="15px" fill="#ffffff">{this.props.name}</text>
            </svg>

        )
    }
}

LinearGauge.defaultProps = {
  value: 0,
  value_unit: "%",
  name: "NaN",
  height: 150,
  width: 100,
  gauge_height: 100,
  gauge_width: 20
}
