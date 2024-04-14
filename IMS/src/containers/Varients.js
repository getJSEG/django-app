import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import { useParams } from "react-router-dom";
import { load_varients } from "../actions/varients";
import VarientItems from "../components/sub_components/VarientItems";

import VarientFormPopup from "../components/sub_components/VarientFormPopup";


const Varients = ({load_varients, varients_global, loading_global}) => {
    const params = useParams();

    const [windowClosed, setWindowClosed] = useState(true)

    const onWindowClose = e => {  setWindowClosed(true)  }
    const openFormWindow = e => { setWindowClosed(false) }
    
    
    useEffect( () => {
        load_varients(params?.id)
    }, []);


    return (
        <div id="varients">
            <div className="varient-nav-buttons">
                <h4 className="varient-title"> Varientes </h4>

                <div onClick={openFormWindow}  className="create-varient-name">
                    <svg xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" className="bi bi-plus" viewBox="-1.5 -2 20 20">
                        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                    </svg>
                    <span className="create-varient-detail"> Añadir </span>
                </div>
            </div>
           
           <ul className="varient-list-container">
            {
                !loading_global ?  varients_global.map( (varient) => { 
                    console.log(varient);
                    return <VarientItems key={varient.id} varient={varient}/>
                }) : <div> Loading </div>
            }
           </ul>

            <VarientFormPopup windowClosed={onWindowClose} isWindowClosed={windowClosed}/>
        </div>
    );
}

const mapStateToProps = state => ({
    varients_global:  state.varients.varients,
    loading_global: state.varients.loading
});

export default connect(mapStateToProps, {load_varients})(Varients);