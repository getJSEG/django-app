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


 export const create_varient = () => async dispatch => {

 }
 
 export const update_varient = (id) => async dispatch => {
 
 }
 
 export const delete_varient = (id) => async dispatch => {
 
 }