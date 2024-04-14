import Cookies from 'js-cookie';
 import {
    CREATE_VARIENT_SUCCESS,
    CREATE_VARIENT_FAIL,
    LOAD_VARIENTS_SUCCESS,
    LOAD_VARIENTS_FAIL,
    UPDATE_VARIENT_SUCCESS,
    UPDATE_VARIENT_FAIL,
    DELETE_VARIENT_SUCCESS,
    DELETE_VARIENT_FAIL
 } from './types';


 export const load_varients = (id) => async dispatch => {

    const requestOptions = {
        method:"GET",
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json",
        },
    };

    try{
        await fetch(`/api/product/${id}/varients`, requestOptions)
        .then( response => { 
            if (response.status >= 200 && response.status <= 299) { 
                return response.json()  
            } 
        })
        .then( data =>  {
            dispatch({
                type: LOAD_VARIENTS_SUCCESS,
                payload: data
            })
        })

    }catch(err) {
        dispatch({ type:LOAD_VARIENTS_FAIL })
    }

 }

 export const create_varient = (product_id, name, size, units, purchasePrice, listedPrice) => async dispatch => {

    const requestOptions = {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get("csrftoken") // this will get cookie
        },
        mode: 'same-origin',
        body: JSON.stringify({ name: name, size: size, units: units, purchase_price: purchasePrice, list_price:listedPrice }),
    };

    try{
        await fetch(`/api/product/${product_id}/create-varient`, requestOptions)
        .then( response => { 
            if (response.status >= 200 && response.status <= 299) { 
                return response.json()  
            } else{
                dispatch({
                    type: CREATE_VARIENT_FAIL,
                    payload: false
                })
            }
        })
        .then( data =>  {
            dispatch({
                type: CREATE_VARIENT_SUCCESS,
                payload: true
            })
        })

    }catch(err) {
        dispatch({ type:CREATE_VARIENT_FAIL })
    }
    

 }
 
 export const update_varient = (id) => async dispatch => {
 
 }
 
 export const delete_varient = (id) => async dispatch => {
 
 }