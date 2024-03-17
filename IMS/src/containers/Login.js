import React, { Component, useState } from "react";

import { login } from '../actions/auth.js';
import { connect } from 'react-redux';
import  { Navigate, useLocation } from 'react-router-dom';
import CSRFToken from '../components/CSRFToken.js';

const Login = ({ login, isAuthenticated, fieldErr_global }) => {
    const [usernameEmpty, setUsernameEmpty] = useState("")
    const [passwordEmpty, setPasswordEmpty] = useState("")
    const location = useLocation();

    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });



    const { username, password } = formData;

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();
        if(!username){ setUsernameEmpty("empty"); } else { setUsernameEmpty("");}
        if(!password){  setPasswordEmpty("empty"); } else { setPasswordEmpty("");}
        login(username, password);
    };

    if (isAuthenticated)
    //TODO: when login out and loggin back in it redirects to 404 page
    // TODO: FIX this proble above
        return <Navigate to={`${location?.state?.prevUrl}`}/>;

    return(
        <div className="container-fluid d-flex g-0 row align-items-center exrra ">
            
            <div id="main-img-container" className="container-lg d-none d-md-block col-md-6 px-0"> </div>

            <div className="container-lg col-md-6 align-middle nopadding row g-0 form-input d-flex justify-content-center">

                <div className="w-100 text-center container-sm col-md-8 ">
                    <img className="w-50 pb-3" src="../static/images/Pink_logo.png"/>
                </div>
                
                <div className="col-md-8 m-0 nopadding">

                    <p className="d-block text-center text-uppercase fs-4 font-weight-normal p-3 text-capitalize">
                        Inicia sesión
                    </p>

                    <span className="main-err-msg"> {fieldErr_global}</span>

                    <form onSubmit={e => onSubmit(e)} className="p-2 d-block align-text-center">
                            <CSRFToken />
                            <span className="err-msg"></span> 
                            <input  className={`form-control mb-3 ${usernameEmpty}`}
                                    name="username"
                                    placeholder="Usuario"
                                    type="text" 
                                    onChange={e => onChange(e)}
                                    value={username}
                                    ></input>
                            <span className="err-msg"></span> 
                            <input className={`form-control mb-3 ${passwordEmpty}`}
                                
                                    name="password"
                                    placeholder="Contraseña"
                                    type="password"
                                    autoComplete="on"
                                    onChange={e => onChange(e)}
                                    value={password}
                                    ></input>
                        
                            <button className="btn btn-primary mt-3" type='submit btn btn-primary mb-3'>
                                INICIAR SESIÓN 
                                {/* <Link className="btn btn-primary" type='submit' to="/main"> INICIAR SESIÓN </Link> */}
                            </button>
                    </form>

                </div>
            </div>
            
        </div>
    );
}


const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
    fieldErr_global : state.auth.fieldErr
});

export default connect(mapStateToProps, {login})(Login);