import * as React from 'react';
import './Slider.scss';

interface Props{
    vertical: boolean
    min: number
    max: number
    callback(val: number): void
}

interface State{
    value: number
}

export default class Slider extends React.Component<Props, State> {
    static defaultProps = {
        vertical: false,
        min: 0,
        max: 100,
        initVal: 50,
        callback: () => {}
    }

    constructor(props) {
        super(props);

        this.state = {
            value: 50
        }

        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(val) {
        this.setState({value: val.target.value});
        this.props.callback(this.state.value);
    }

    render() {
        return (
            <input type='range' 
                min={this.props.min} 
                max={this.props.max}
                value={this.state.value}
                className='slider'
                onChange={this.handleChange}
            />
        )
    }

}
