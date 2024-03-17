import React from "react";
import { NavLink } from "react-router-dom";


const PageNotFound = () => {
    return(
        <div className="PageNotFound">
            <h1>404</h1>

            <h5>PAGE NOT FOUND</h5>

            
            <p> 
                Esta Pagina no fue encontrada 
                porfavor regesa a la pagina principal
            </p>
            
            <NavLink className="pagenotfoun-btn" to='/dashboard'>
                Regresar a donde estabas.
            </NavLink>
        </div>
    )
}

export default PageNotFound