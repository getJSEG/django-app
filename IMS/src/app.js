import React, { Component } from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route, Links } from "react-router-dom";

import Login from "./containers/Login";
import Profile from "./components/Profile";
import Dashboard from "./components/Dashboard";
import Menu from "./containers/Menu";
import Inventory from "./containers/Inventory";
import Search from "./containers/Search";
import Sales from "./containers/Sales";
import Varients from "./containers/Varients";
import PageNotFound from "./components/PageNotFound";
import CreateProductForm from "./components/sub_components/CreateProductForm"


import PrivateRoute from "./hocs/PrivateRoute";

import  { Provider } from 'react-redux';
import store from './store';


const root = ReactDOM.createRoot(document.getElementById("root"));

export default class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return(
            <Provider store={store}>
                <Router>
                    <Routes>

                        <Route element={ <PrivateRoute /> } > 
                            <Route exact path='/dashboard' element={ <Dashboard /> } /> 
                            <Route exact path='/inventory' element={ <Inventory /> } />
                            <Route exact path='/menu' element={ <Menu /> } />
                            <Route exact path='/search' element={ <Search /> } />
                            <Route exact path='/sales' element={ <Sales /> } />
                            <Route exact path='/create-product' element={ <CreateProductForm /> } />
                            <Route exact path='/product/:id/varients' element={ <Varients /> } />
                        </Route>

                        <Route exact path="/login" element={<Login />} /> 
                        <Route path="*" element={<PageNotFound /> } />

                    </Routes>
                </Router>
            </Provider>
        )
    }
}
root.render( <React.StrictMode> <App /> </React.StrictMode> );