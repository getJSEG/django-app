import React from "react"
import { connect } from "react-redux"
import { useLocation, NavLink, useParams} from 'react-router-dom';

const VarientItems = ({varient}) => {

    const params = useParams();

    return(
        <li className="varient-item-container">
               <NavLink className="varient-lnk" to={`/product/${varient.id}/varients`}>
                    <div className="varient-img-container">
                        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="#fff" className="bi bi-file-earmark-image missing-img" viewBox="-2.5 -1 20 20">
                            <path d="M6.502 7a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3"/>
                            <path d="M14 14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zM4 1a1 1 0 0 0-1 1v10l2.224-2.224a.5.5 0 0 1 .61-.075L8 11l2.157-3.02a.5.5 0 0 1 .76-.063L13 10V4.5h-2A1.5 1.5 0 0 1 9.5 3V1z"/>
                        </svg>
                    </div>

                        <div className="varient-info-con">
                            <p className="varient-name">{varient.name}</p>

                            <div className="varient-information-con">
                                <div className="varient-info-overview">
                                    <p className="varient-in varient-sku">Sku: <span className="info">{ varient.sku }</span> </p>
                                    <p className="varient-in varient-size"> Size: <span className="info">{ varient.size }</span> </p>
                                </div>
                                <div className="varient-info-overview">
                                    <p className="varient-in varient-units">Unidades: <span className="info">{ varient.units }</span> </p>
                                    <p className="varient-in varient-price">Precio: <span className="info"> ${ varient.price }</span> </p>
                                </div>
                            </div>
                        </div>
                
               </NavLink>
        </li>
    );
};

export default connect(null, {})(VarientItems);