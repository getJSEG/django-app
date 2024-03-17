import React from "react";
import { connect } from "react-redux";


const Sales = () => {
    return (
        <div id="sales-container">
           <div className="sales-nav-container">
                <h4 className="sales-title"> Ventas </h4>
            </div>

            <div>
                <p>Esta función aún no está disponible</p>
            </div>
        </div>
    );
}


export default connect(null, {})(Sales);