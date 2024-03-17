import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import { useParams } from 'react-router-dom';
import Product from "../components/sub_components/Product";
import { load_product } from "../actions/products";
// import { create_product } from "../actions/products";


const Invetory = ({product_global, load_product, })=>{
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    const [productNameEmpty, setproductNamempty] = useState("")
    const [productBrandEmpty, setproductBrandEmpty] = useState("")

    const [closeWindow, setCloseWindow] = useState("closeWindow")

    const [formData, setFormData] = useState({
        productName: '',
        brandName: '',
    });

    const {productName, brandName} = formData;

    const onChange = e => setFormData({... formData, [e.target.name]: e.target.value })

    const onWindowClose = e => { setCloseWindow("closeWindow") }

    const openFormWindow = e => { setCloseWindow("open") }

    const onSubmit = e => {
        e.preventDefault();
        console.log("runs")
        // create_product(productName, brandName)
    }

    useEffect(() => {
        load_product().then( rr => {
            setLoading(false)
        })
      }, []);

    return(
        <div id="inventory"> 

            <div className="inventory-nav-buttons">
                <h4 className="inventory-title"> Inventario </h4>
                
                <div className="create-product-desk">
                    <svg xmlns="http://www.w3.org/2000/svg" width="45" height="45" fill="currentColor" className="bi bi-plus" viewBox="-1.5 -2 20 20">
                        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                    </svg>
                    <span> Añadir </span>
                </div>

            </div>

            <div className="inventory-overview">
                <div className="inventory-summary product-qty">
                    <p className="overview-name"> Products </p>
                    <p className="overview-info"> { loading ? "" : product_global.length }</p>
                </div>

                <div className="inventory-summary  varient-qty">
                    <p className="overview-name"> Varientes </p>
                    <p className="overview-info"> 2 </p>
                </div>

                <div className="inventory-summary  unit">
                    <p className="overview-name"> unidades</p>
                    <p className="overview-info"> 1 </p>
                </div>

                <div className="inventory-summary  total-calue">
                    <p className="overview-name"> valor </p>
                    <p className="overview-info"> 1</p>
                </div>
            </div>

            <ul className="product-list">
                { loading ? "Loading Page" : ( product_global.map( (product) =>  <Product key={product.id} product={product}/>  ) ) }
            </ul>

            <div className="create-product-button-m"> 
                <svg onClick={openFormWindow} xmlns="http://www.w3.org/2000/svg" width="55" height="55" fill="currentColor" className="bi bi-plus" viewBox="-1.75 -2 20 20">
                    <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                </svg>
            </div>


            <span className={`pop-up-blur ${closeWindow}`}> </span>

            <div className={`pop-form-create-product ${closeWindow}`}>

                <div className="pop-form-close-btn">
                    <svg onClick={onWindowClose} xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="bi bi-x-lg" viewBox="0 0 20 20">
                        <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
                    </svg>
                </div>
                <form onSubmit={e => onSubmit(e)}  className="pop-up-product-form">
                    <input  className='product-fiel-input mb-3 form-control'
                            name="productName"
                            placeholder="Product Name"
                            type="text" 
                            onChange={e => onChange(e)}
                            value={productName}
                            ></input>

                    <input className="product-fiel-input mb-3"
                            name="brandName"
                            placeholder="Marca"
                            type="text"
                            autoComplete="on"
                            onChange={e => onChange(e)}
                            value={brandName}
                            ></input>

                    <button className="pop-up-create-product-button" type='submit'>
                        Crear Producto
                    </button>
                </form>
            </div>

        </div>
    )
}

const mapStateprops = state => ({
    product_global:  state.products.product
});



export default connect(mapStateprops, {load_product})(Invetory);