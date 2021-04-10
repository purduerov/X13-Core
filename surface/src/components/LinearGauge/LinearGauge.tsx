import * as React from 'react';
import './LinearGauge.scss';

interface Props{
    value: number
    units: string
    name: string
    width: number
    height: number
    gWidth: number
    gHeight: number,
    inverted: boolean
}

export default class LinearGauge extends React.Component<Props, {}> {
    static defaultProps = {
        value: 0,
        units: '%',
        name: '',
        width: 100,
        height: 150,
        gWidth: 20,
        gHeight: 100,
        inverted: false
    }

    render() {
        let shiftH = this.props.height / 6;
        let shiftW = this.props.width / 4;
        let tickH = this.props.gWidth / 2;
        let tickW = this.props.gHeight / 5;
        let textW = (this.props.width * 4) / 7;
        let textH = (this.props.width * 7) / 10;
        let textHN = (this.props.width * 9) / 10;
        let tick = `0,-${tickH} 0,${tickH} ${tickW},0`;

        let fg;
        let tri;

        `translate(0,${this.props.gHeight + shiftH - this.props.value})`

        if(this.props.inverted){
            fg = <rect width={this.props.gWidth} height={this.props.value} fill="#A6A6A6"></rect>;
            tri = <g transform={`translate(0,${shiftH + this.props.value})`}>
                    <polygon points={tick} fill="#807E7E"/>
                  </g>;

        }else{
            fg = <rect width={this.props.gWidth} height={this.props.gHeight - this.props.value} fill='#A6A6A6'></rect>;
            tri = <g transform={`translate(0,${this.props.gHeight + shiftH - this.props.value})`}>
                    <polygon points={tick} fill='#807E7E'/>
                  </g>;
        }
        return (
            <svg width={this.props.width} height={this.props.height}>
                <g>
                    <svg width={this.props.gWidth} height={this.props.gHeight} x={shiftW} y={shiftH}>
                        <rect width={this.props.gWidth} height={this.props.gHeight} fill='#39B4CC'></rect>
                        {fg}
                    </svg>
                </g>
                {tri}

                <text x={textW} y={textH}>{`${this.props.value}${this.props.units}`}</text>
                <text x={textW} y={textHN}>{this.props.name}</text>
            </svg>
        );
    }
}
