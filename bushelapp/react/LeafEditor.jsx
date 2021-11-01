import React from "react";
import BacklinksContainer from "./BacklinksContainer";
import Markdown from "./Markdown";

class LeafEditor extends React.Component {
    constructor(props) {
        super(props);

        const queryString = new URLSearchParams(this.props.location.search);

        this.state = {
            leaf: {
                id: 0,
                name: "Untitled Leaf",
                uri: queryString.get('leaf'),
                text: "# Untitled Leaf\nThis is a new untitled leaf.",
            },
            branch: {
                id: 0,
                name: "Untitled Branch",
                uri: "untitled-branch",
            },
            root: {
                id: 0,
                uri: "untitled-root"
            },
            updateEditor: false
        };

        this.GetLeafData();
    }

    GetLeafData = async () => {
        let leaf_uri = this.state.leaf.uri;
        console.log("Getting leaf data...");
        // get leaf information from bushel's API
        fetch('api/leaves/' + leaf_uri)
        .then(response => response.json())
        .then(data => {
            return {leaf: 
                {
                    id: data.id,
                    name: data.name,
                    uri: leaf_uri,
                    text: data.plaintext,
                },
                branch: {
                    id: data.branch.id,
                    name: data.branch.name,
                    uri: data.branch.uri,
                },
                root: {
                    id: data.branch.root.id,
                    uri: data.branch.root.uri
                }
            }
        })
        .then(data => this.setState({
            leaf: data.leaf,
            branch: data.branch,
            root: data.root,
            updateEditor: true
        }))
        .then(() => console.log("Got leaf data!"))
        .catch(error => console.log(error));
    }

    SaveLeaf = (leafName) => {
        console.log("leaf saved!");
        let leaf = this.state.leaf;
        leaf.name = leafName;
        this.setState({
            leaf: leaf,
            branch: this.state.branch,
            root: this.state.root,
            updateEditor: false
        });
        console.log(this.state.leaf);
    }

    UpdateBody = (text) => {
        let leaf = this.state.leaf;
        leaf.text = text;
        this.setState({
            leaf: leaf,
            branch: this.state.branch,
            root: this.state.root,
            updateEditor: false
        });
        console.log
    }

    handleUriChange = (e) =>
    {
        let leaf = this.state.leaf;
        leaf.uri = e.target.value;
        this.setState({leaf: leaf });
    }

    render () {
        return (
            <div>   
                <div className="edit-bar">
                    <ul className="edit-bar-nav-list horizontal-scroll">
                    <li className="edit-bar-item">
                            <a className="" href="">
                                <span>{this.state.root.uri}</span>
                            </a>
                        </li>
                        <li className="edit-bar-item list-separator">/</li>
                        <li className="edit-bar-item">
                            <a className="" href="">
                                <span>{this.state.branch.uri}</span>
                            </a>
                        </li>
                        <li className="edit-bar-item list-separator">/</li>
                        <li className="edit-bar-item">
                            <input className="input"
                                value={this.state.leaf.uri}
                                onChange={this.handleUriChange} />
                        </li>
                    </ul>
                    <span className="nav-bar-spacer"></span>
                    <ul className="edit-bar-nav-list">
                        <li className="edit-bar-button">
                            <a className="button-light" href={"/" + this.state.root.uri + "/" + this.state.branch.uri + "/" + this.state.leaf.uri}>
                                <span>Return</span>
                            </a>
                        </li>
                        <li className="edit-bar-button">
                            <a className="button-light" href={"/auth/logout?next=/" + this.state.root.uri + "/" + this.state.branch.uri + "/" + this.state.leaf.uri}>
                                <span>Logout</span>
                            </a>
                        </li>
                    </ul>
                </div>
                <div className="page-body">
                    <div className="content-body">
                        <Markdown text={this.state.leaf.text} updateCallback={this.UpdateBody} doUpdate={this.state.updateEditor} />
                    </div>
                    <div className="backlinks">
                        <BacklinksContainer leafName={this.state.leaf.name} saveCallback={this.SaveLeaf}/>
                    </div>
                </div>
            </div>
        );
    }
}
export default LeafEditor;