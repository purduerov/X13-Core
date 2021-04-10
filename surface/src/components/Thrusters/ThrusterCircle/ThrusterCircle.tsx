import * as React from 'react';
import './ThrusterCircle.scss';

interface Props{
    thrust: number
    className: string
    name: string
}

export default class ThrusterCircle extends React.Component<Props, {}> {
    circleStyle: {}

	constructor(props: Props) {
        super(props);

        this.circleStyle = {
            backgroundImage: 'linear-gradient(91deg, transparent 50%, #A6A6A6 50%), linear-gradient(90deg, #A6A6A6 50%, transparent 50%)'
        };

        this.setValue = this.setValue.bind(this);
		this.setValue();

    }

    componentDidUpdate(){
        this.setValue();
    }

    setValue() {
		var color = '#39B4CC';
		if(this.props.thrust < 127){
			color = '#FF4747';
		}
		var output = Math.round((Math.abs(this.props.thrust - 127) / 127) * 360);

        if(output <= 180){
            this.circleStyle = {
                backgroundImage: 'linear-gradient(' + (output + 90) +'deg, transparent 50%, #A6A6A6 50%),linear-gradient(90deg, #A6A6A6 50%, transparent 50%)',
				backgroundColor: color
			};
        }else{
            this.circleStyle = {
                backgroundImage: 'linear-gradient(' + (output - 90) +'deg, transparent 50%, ' + color + ' 50%),linear-gradient(90deg, #A6A6A6 50%, transparent 50%)',
				backgroundColor: color
			};
        }
    }

	render() {
		return (
			<div className={this.props.className}>
                <div className='active-border' style={this.circleStyle}>
                    <div className='circle'>
                        <span className='val 360'>{Math.round(((Math.abs(this.props.thrust) - 127) / 127) * 100)}%</span>
						<br/>
						<span className='val 360'>{this.props.name}</span>
                    </div>
                </div>
			</div>
		);
	}
}
