import Cookies from 'js-cookie';
import {
    CREATE_PRODUCT_SUCCESS,
    CREATE_PRODUCT_FAIL,
    LOAD_PRODUCTS_SUCCESS,
    LOAD_PRODUCTS_FAIL,
    UPDATE_PRODUCT_SUCCESS,
    UPDATE_PRODUCT_FAIL,
    DELETE_PRODUCT_SUCCESS,
    DELETE_PRODUCT_FAIL 

} from './types';
import { response } from 'express';


export const load_product = () => async dispatch => {
    const requestOptions = {
        method:"GET",
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json"
        }
    };

    try{
        await fetch('/api/products',requestOptions)
        .then( response => { 
            if (response.status >= 200 && response.status <= 299) { 
                return response.json()  
            } 
        })
        .then( data =>  {
            dispatch({
                type: LOAD_PRODUCTS_SUCCESS,
                payload: data
            })
        })

    }catch(err) {
        dispatch({ type:LOAD_PRODUCTS_FAIL })
    }
}

export const create_product = (product_name, product_brand) => async dispatch => {
    // const requestOptions = {
    //     method: "POST",
    //     headers: {
    //         'Accept': 'application/json',
    //         "Content-Type": "application/json",
    //         "X-CSRFToken": Cookies.get("csrftoken") // this will get cookie
    //     },
    //     mode: 'same-origin',
    //     body: JSON.stringify({ name: product_name, brand: product_brand }),
    // };

    // try{
    //     await fetch('/api/createproduct',requestOptions)
    //     .then(response => {
    //         if(response.status >= 200 && response.status <= 299){
    //             return esponse.json()
    //         }
    //     })
    //     .then( data => {
    //         dispatch({
    //             type:CREATE_PRODUCT_SUCCESS,
    //             payload: data
    //         })
    //     })

    // }catch(err){
    //     dispatch({
    //         type: CREATE_PRODUCT_FAIL
    //     })
    // }

}

export const update_product = () => async dispatch => {

}

export const delete_product = () => async dispatch => {

}