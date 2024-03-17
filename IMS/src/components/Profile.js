import React, { Component, useState } from "react";
// import Login from './Login';
import PropTypes from 'prop-types';
// import Cookies from 'universal-cookie';
import  { Navigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';
import  { Provider } from 'react-redux';


export default class Profile extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            password: "",
            isAuthenticated: false,
            session: Cookies.get("sessionid")
        }

    }

    render = () => {
       
        return (
            <div> 
                <h1> 4EVER LOGO </h1>

                <nav> 
                    <ul>
                        <li> Locales </li>
                        <li> Productos </li>
                        <li> Inventario </li>
                        <li> Ventas </li>
                    </ul>
                </nav>

                <button 
                    className="btn btn-primary mt-3"
                    id="submit"
                    type='submit btn btn-primary mb-3'
                    >
                    TERMINAR SESIÓN
                </button>
            </div>

        );
    }
}