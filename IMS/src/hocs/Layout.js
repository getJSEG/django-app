import React, { useEffect, Fragment } from 'react';
import Navbar from '../components/sub_components/Navbar';
import { connect } from 'react-redux';


const Layout = ({ children }) => {
    return (
        <Fragment>
            <Navbar />
            {children}
        </Fragment>
    );
};

export default connect(null,{})(Layout);