import React, { useState, useEffect, useCallback }from "react";

import { connect } from "react-redux";


const VarientFormPopup  = ({windowClosed, isWindowClosed}) => {
    
    const [varientName, setvarientName] = useState('');
    const [size, setSize] = useState('');
    const [units, setUnits] = useState('');
    const [color, setColor] = useState('');
    const [purchasePrice, setpPrice] = useState('');
    const [listedPrice, setLPrice] = useState('');
    const [images, setImages] = useState([]);


    const getFiles = e => {
        setImages([...images, ...e.target.files])
    }

    const onChange = e => {
        console.log(e.target.name)
        switch(e.target.name){
            case 'varientName':
                setvarientName(e.target.value);
                break;
            case 'size':
                setSize(e.target.value)
                break;
            case 'units':
                setUnits(e.target.value)
                break;
            case 'purchasePrice':
                setpPrice(e.target.value)
                break;
            case 'listedPrice':
                setLPrice(e.target.value)
            default:
                break;
        };
    }

    const onSubmit = e => {
        e.preventDefault();

    }

    return(
        <div>
            <span className={`pop-up-blur ${ isWindowClosed ? "varient-Form-close" : "varient-form-open"}`}> </span>

            <div id="varient-form-popup" className={`pop-form-create-product ${ isWindowClosed ? "varient-Form-close" : "varient-form-open"}`}>

                <div className="pop-form-close-btn">
                    <svg onClick={windowClosed} xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" className="bi bi-x-lg" viewBox="0 0 20 20">
                        <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
                    </svg>
                </div>
                    <form onSubmit={e => onSubmit(e)} className="pop-up-product-form">
                        <input  className='product-fiel-input mb-3 form-control'
                                name="varientName"
                                placeholder="Nombre"
                                type="text" 
                                onChange={e => onChange(e)}
                                value={varientName}
                                ></input>

                        <input className="product-fiel-input mb-3"
                                name="size"
                                placeholder="Tallas"
                                type="text"
                                autoComplete="on"
                                onChange={e => onChange(e)}
                                value={size}
                                ></input>

                        <input className="product-fiel-input mb-3"
                                name="units"
                                placeholder="Unidades"
                                type="text"
                                autoComplete="on"
                                onChange={e => onChange(e)}
                                value={units}
                                ></input>

                        <input className="product-fiel-input mb-3"
                                name="purchasePrice"
                                placeholder="Precio de Compra"
                                type="text"
                                autoComplete="on"
                                onChange={e => onChange(e)}
                                value={purchasePrice}
                                ></input>

                        <input className="product-fiel-input mb-3"
                                name="listedPrice"
                                placeholder="Precio Al Cliente"
                                type="text"
                                autoComplete="on"
                                onChange={e => onChange(e)}
                                value={listedPrice}
                                ></input>

                        <input className="product-fiel-input mb-3"
                                name="images"
                                type="file"
                                multiple
                                autoComplete="on"
                                onChange={e => getFiles(e)}
                                ></input>

                        <button className="pop-up-create-product-button" type='submit'>
                            Crear Producto
                        </button>
                    </form>
            </div>
        </div>
    );
}

export default connect(null, {})(VarientFormPopup);