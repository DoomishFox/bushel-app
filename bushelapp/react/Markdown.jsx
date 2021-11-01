import React from 'react';

class Markdown extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            text: props.text
        };
    }

    componentDidUpdate(prevProps) {
        if (this.props.doUpdate){
            this.setState({text: this.props.text});
            this.props.updateCallback(this.state.text);
        }
    }

    handleChange = (e) => {
        this.setState({ text: e.target.value });
    }

    render() {
        return (
            <div>
                <textarea className="fill-width"
                    onChange={this.handleChange}
                    value={this.state.text} />
                <hr />
                <div className="backlinks-content">
                    <button className="button fill-width"
                        onClick={() => this.props.updateCallback(this.state.text)}>
                        <span>Update</span>
                    </button>
                </div>
            </div>
        );
    }
}
export default Markdown;