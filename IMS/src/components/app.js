import React, { Component } from "react";
import {render } from "react-dom";
import HomePage from "./Homepage";

import { BrowserRouter as Router, Routes, Route, Links, Redirect} from "react-router-dom";

export default class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return(
            <Router>
                <Routes>
                    <Route path="/" element={<HomePage /> } />
                    <Route path="/main" element={<HomePage /> } />
                </Routes>
            </Router>
        )
    }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);