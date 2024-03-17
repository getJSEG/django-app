import React from "react"
import { connect } from "react-redux"
import { useLocation, NavLink, useParams} from 'react-router-dom';

// TODO: Create a link to  to show all paroduct varients
//TODO: <NavLink />
const Product = ({product}) => {

    const params = useParams();

    console.log(params)



    return(
        <li className="product">
               <NavLink className="product-lnk" to={`/product/${product.id}/varients`}>
                    <div className="product-img-container">
                            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="#fff" className="bi bi-file-earmark-image missing-img" viewBox="-2.5 -1 20 20">
                                <path d="M6.502 7a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3"/>
                                <path d="M14 14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zM4 1a1 1 0 0 0-1 1v10l2.224-2.224a.5.5 0 0 1 .61-.075L8 11l2.157-3.02a.5.5 0 0 1 .76-.063L13 10V4.5h-2A1.5 1.5 0 0 1 9.5 3V1z"/>
                            </svg>
                        </div>
                        <div className="product-info">
                            <p className="sku"> sku  </p>
                            <p className="product-name">{product.name}</p>
                            <p className="varient-qty">10 units</p>
                        </div>
                
                        
                        <div className="product-options">
                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3"/>
                            </svg>
                        </div>
               </NavLink>
        </li>
    );
};

export default connect(null, {})(Product);