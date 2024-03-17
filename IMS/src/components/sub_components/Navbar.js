import React, { Fragment } from "react";
import { Link, NavLink } from "react-router-dom";
import { connect } from "react-redux";
import { logout } from '../../actions/auth';

const navbar = ({ isAuthenticated,avatar_global,  logout }) => {


    const authLinks = (
        <Fragment>
            <div className="avatar-container">
                <img  className="avatar" src='../../static/images/menu/user_icon.png'/>
            </div>

            <li className="li-container"> 
                <NavLink className="dashboard-link nav-links" to="/dashboard"> 
                    <svg  xmlns="http://www.w3.org/2000/svg" className="nav-i-c-a-c" width="24" height="25" fill="none" viewBox="15 15 20 20">
                        <path strokeMiterlimit="10" strokeOpacity=".8" strokeWidth="1.5" d="M21.5 21h-4c-.828 0-1.5-.746-1.5-1.667v-1.666c0-.92.672-1.667 1.5-1.667h4c.828 0 1.5.746 1.5 1.667v1.666c0 .92-.672 1.667-1.5 1.667zM21.5 32h-4c-.828 0-1.5-.566-1.5-1.263v-5.474c0-.698.672-1.263 1.5-1.263h4c.828 0 1.5.566 1.5 1.263v5.474c0 .698-.672 1.263-1.5 1.263zM30.714 27h-3.428c-.71 0-1.286.746-1.286 1.667v1.666c0 .92.576 1.667 1.286 1.667h3.428c.71 0 1.286-.746 1.286-1.667v-1.666c0-.92-.576-1.667-1.286-1.667zM30.714 16h-3.428c-.71 0-1.286.566-1.286 1.263v5.474c0 .698.576 1.263 1.286 1.263h3.428c.71 0 1.286-.566 1.286-1.263v-5.474c0-.698-.576-1.263-1.286-1.263z"></path>
                    </svg>
                    <p className="icon-name nav-i-c-a-c"> Tablero </p>
                </NavLink>
            </li>

            <li className="li-container">
                <NavLink className="products nav-links" to="/inventory"> 
                    <svg xmlns="http://www.w3.org/2000/svg" className="nav-i-c-a-c" width="24" height="24" fill="none" viewBox="15 15 20 20">
                        <path strokeLinejoin="round" strokeMiterlimit="10" strokeOpacity=".8" strokeWidth="1.514" d="M16.045 19.488h15.91"></path>
                        <path strokeLinecap="round" strokeLinejoin="round" strokeMiterlimit="10" strokeOpacity=".8" strokeWidth="1.514" d="M19.325 16.164h9.589c.423 0 .824.187 1.095.512l1.617 1.94c.213.257.33.58.33.913v10.408c0 1.049-.85 1.9-1.9 1.9H18.183c-1.05 0-1.9-.851-1.9-1.9V19.529c0-.334.117-.656.33-.912l1.617-1.941c.271-.325.672-.512 1.095-.512zM21.98 22.812h4.275M24.12 16.4v2.85"></path>
                    </svg>
                    <p className="icon-name nav-i-c-a-c"> Inventario </p>
                </NavLink>
            </li>

            <li className="li-container">
                <NavLink className="buscar nav-links" to="/search"> 
                    <svg xmlns="http://www.w3.org/2000/svg" className="nav-i-c-a-c" width="23" height="23" fill="none" viewBox="15 15 20 20">
                        <path  strokeMiterlimit="10" strokeOpacity=".8" strokeWidth="1.534" d="M23.308 30.51c3.978 0 7.203-3.224 7.203-7.203 0-3.978-3.225-7.202-7.203-7.202-3.979 0-7.203 3.224-7.203 7.203 0 3.978 3.224 7.203 7.203 7.203z"></path>
                        <path  strokeLinecap="round" strokeMiterlimit="10" strokeOpacity=".8" strokeWidth="1.534" d="M28.4 28.4l3.495 3.495"></path>
                    </svg>
                    <p className="icon-name nav-i-c-a-c"> Buscar </p>
                </NavLink>
            </li>

            <li className="li-container">
                <NavLink className="ventas nav-links" to="/sales"> 
                    <svg xmlns="http://www.w3.org/2000/svg" className="nav-i-c-a-c" width="24" height="24" fill="none" viewBox="0 0 20 20">
                        <path strokeLinecap="round" strokeMiterlimit="8" strokeOpacity=".8" d="M0 0h1v15h15v1H0zm10 3.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-1 0V4.9l-3.613 4.417a.5.5 0 0 1-.74.037L7.06 6.767l-3.656 5.027a.5.5 0 0 1-.808-.588l4-5.5a.5.5 0 0 1 .758-.06l2.609 2.61L13.445 4H10.5a.5.5 0 0 1-.5-.5"/>
                    </svg>
                    <p className="icon-name nav-i-c-a-c"> ventas </p>
                </NavLink>
            </li>

            <li className="li-container">
                <NavLink className="menu nav-links" to="/menu"> 
                    <svg xmlns="http://www.w3.org/2000/svg" className="nav-i-c-a-c" width="24" height="24" fill="none"  viewBox="0 0 15 15">
                        <path strokeLinecap="round" strokeMiterlimit="10" strokeOpacity=".8" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/>
                    </svg>
                    <p className="icon-name nav-i-c-a-c"> Menu </p>
                </NavLink>
            </li>

            <li className="logout-container li-container">
                <a className="logout-link" onClick={logout} href="/login"> 
                    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="#262626" viewBox="-2 0 20 20">
                        <path fillRule="evenodd" d="M3.5 6a.5.5 0 0 0-.5.5v8a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5v-8a.5.5 0 0 0-.5-.5h-2a.5.5 0 0 1 0-1h2A1.5 1.5 0 0 1 14 6.5v8a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 14.5v-8A1.5 1.5 0 0 1 3.5 5h2a.5.5 0 0 1 0 1z"/>
                        <path fillRule="evenodd" d="M7.646.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 1.707V10.5a.5.5 0 0 1-1 0V1.707L5.354 3.854a.5.5 0 1 1-.708-.708z"/>
                    </svg>
                    <p className="logout-name"> Cerrar Sesión </p>
                </a>
            </li>
        </Fragment>
    );

    const guestLinks = (
        <Fragment>
        </Fragment>
    );

    return(
        <nav id="navigation">


            { isAuthenticated ? authLinks : guestLinks}
        </nav>
    );
}

const mapStateToProps = state =>({
    isAuthenticated: state.auth.isAuthenticated,
    avatar_global: state.profile.avatar,
});



export default connect(mapStateToProps, { logout }) (navbar);