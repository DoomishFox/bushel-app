import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Route } from "react-router-dom";
import LeafEditor from "./LeafEditor";
  
ReactDOM.render(
    <Router>
        <Route path="/" component={LeafEditor} />
    </Router>,
    document.getElementById("react-root")
);