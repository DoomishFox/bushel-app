import React from 'react';

class BacklinksContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            leafName: props.leafName
        };
    }

    componentDidUpdate(prevProps) {
        if (this.props.leafName != prevProps.leafName)
            this.setState({leafName: this.props.leafName});
    }

    handleChange = (e) => {
        this.setState({ leafName: e.target.value });
    }

    render() {
        return (
            <div>
                <input className="input fill-width"
                    placeholder="Leaf name"
                    value={this.state.leafName}
                    onChange={this.handleChange} />
                <hr />
                <div className="backlinks-content">
                    <button className="button fill-width"
                        onClick={() => this.props.saveCallback(this.state.leafName)}>
                        <span>Save Leaf</span>
                    </button>
                </div>
            </div>
        );
    }
}
export default BacklinksContainer;