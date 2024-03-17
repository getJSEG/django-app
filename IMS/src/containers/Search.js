import React from "react";
import { connect } from "react-redux";


const Search = () => {

    return(
        <div id="search-container">
            <div className="search-nav-container">
                <h4 className="search-title"> Buscador </h4>
            </div>

            <div>
                <p>Esta función aún no está disponible</p>
            </div>
        </div>
    )
}

export default connect(null,{})(Search);