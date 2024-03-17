import React, { useEffect, Fragment } from "react";
import { Navigate, Outlet, useLocation} from 'react-router-dom';
import Layout from "./Layout";
import { checkAuthenticated } from '../actions/auth';
import { load_user } from '../actions/profile';


import { connect } from "react-redux";

const PrivateRoute = ({checkAuthenticated, load_user, isAuthenticated }) => {
    const location = useLocation();

    useEffect(() => {
        checkAuthenticated();
        load_user();
    }, []);
    
    return isAuthenticated ? <Layout> <Outlet/>  </Layout>: <Navigate to='/login' state={{prevUrl: location.pathname}} />
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps,  { checkAuthenticated, load_user, })(PrivateRoute);