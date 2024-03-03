import React, { Component } from "react";

export default class Loggin extends Component {
    constructor(props) {
        super(props);
    }

    

    render() {
        return(
            <div className="container-fluid d-flex g-0 row align-items-center exrra ">
                
                <div className=" d-none d-md-block container-lg h-100 col-md-8 nopadding px-0 sign-in-img-con">
                    <img className="img-fluid w-100" src="https://i.pinimg.com/originals/0d/9a/58/0d9a585fd1782e1451af95db30044bcc.jpg" alt="Girl in a jacket" width="500" height="600"/>
                </div>

                <div className="container-lg col-md-4 align-middle nopadding row g-0 form-input d-flex justify-content-center">

                    <div className="w-100 text-center container-sm col-md-8 ">
                        <img className="w-75 pb-3" src="../static/images/Pink_logo.png"/>
                    </div>
                    
                    <div className="w-100 container-lg col-md-8 m-0 nopadding form-input">

                        <p className="d-block
                                      text-center
                                      text-uppercase
                                      fs-4
                                      font-weight-normal
                                      p-3
                                      text-capitalize"> Inicia sesión </p>
                        
                        <form className="w-100 p-2 d-block align-text-center">
                                
                                <input  className="form-control mb-3"
                                        name="Usuario"
                                        placeholder="Usuario"
                                        type="text" ></input>
                            
                                <input className="form-control mb-3"
                                        name="password"
                                        placeholder="Contraseña"
                                        type="password"
                                        autocomplete="on"></input>
                            
                        
                                <input 
                                    className="btn btn-primary mt-3"
                                    id="submit"
                                    type='btn btn-primary mb-3' value='INICIAR SESIÓN' />
                      
                        </form>
                    </div>
                </div>
                
            </div>
        );
    }
}
