import React, { useState, useEffect }from "react";
import { Link, NavLink } from "react-router-dom";
import { connect } from 'react-redux';
import { logout } from '../actions/auth';

const Dashboard  = ({ delete_account, update_profile, first_name_global, last_name_global }) => {
    return(
      <div id="dashboard-container">

        <div className="dashboard-nav-container">
                <h4 className="dashboard-title"> Buscador </h4>
        </div>

       <div> Nombre: {`${first_name_global }`} {`${last_name_global }`} </div>

        <div>
            
            <h4> Invetory Summary </h4>
            <div> 
                <p> productos  </p>
                <p> 2 </p>
            </div>

            <div> 
                <p> Varientes </p>
                <p> 2 </p>
            </div>
            <div>
                <p>Invetory Total</p>
                <p> 20 </p>
            </div>

            <div>
                <p> Valor </p>
                <p> $20 </p>
            </div>

        </div>
        


      </div>  
    )
}


const mapStateToProps = state => ({
    first_name_global: state.profile.first_name,
    last_name_global: state.profile.last_name
});


export default connect(mapStateToProps, {})(Dashboard);