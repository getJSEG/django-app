import React from "react";
import { connect } from "react-redux";


const CreateProductForm = () => {
    return (
        <div id="create-form-container">
            <div className="form-container">
                <form className="product-form">
                    <span className="err-msg"></span> 

                    <input  className='form-control mb-3'
                            name="name"
                            placeholder="Product Name"
                            type="text" 
                            // onChange={e => onChange(e)}
                            value=""
                            ></input>
                    <span className="err-msg"></span> 

                    <input className="form-control mb-3"
                            name="brand"
                            placeholder="Marca"
                            type="text"
                            autoComplete="on"
                            // onChange={e => onChange(e)}
                            value=""
                            ></input>
                
                    <button className="create-product-button" type='submit btn btn-primary mb-3'>
                        Crear Producto
                    </button>

                </form>
            </div>
        </div>
    )
}

export default connect(null, {})(CreateProductForm)