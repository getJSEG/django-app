import Cookies from 'js-cookie';
import { load_user } from './profile';
import axios from 'axios';
import { load_product } from './products';
import {
    REGISTER_SUCCESS,
    REGISTER_FAIL,
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOGOUT_SUCCESS,
    LOGOUT_FAIL,
    AUTHENTICATED_SUCCESS,
    AUTHENTICATED_FAIL,
    DELETE_USER_SUCCESS,
    DELETE_USER_FAIL
} from './types';

export const checkAuthenticated = () => async dispatch =>  {
    const requestOptions = {
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json",
        }
    };

    try {

        const response = await axios.get("/api/authenticated", requestOptions)
        // await fetch("/api/authenticated",requestOptions)
        if (response.status >= 200 && response.status <= 299) { dispatch({ type: AUTHENTICATED_SUCCESS, payload: true }); }
        else if (!response.status >= 200 && !response.status <= 299) { dispatch({ type: AUTHENTICATED_FAIL, payload: false }); }
        else{ dispatch({ type: AUTHENTICATED_FAIL, payload: false }); }
        // .then( data => {
        //     if (!data.status >= 200 && !data.status <= 299) {
        //         dispatch({ type: AUTHENTICATED_FAIL, payload: false });
        //     }
        //     else if (data.status >= 200 && data.status <= 299) {
        //         dispatch({ type: AUTHENTICATED_SUCCESS, payload: true });
        //     }
        //     else {
        //         dispatch({ type: AUTHENTICATED_FAIL, payload: false });
        //     }
        // })

    }catch(err) {
        dispatch({ type: AUTHENTICATED_FAIL, payload: false });
    }


}

export const login = (username, password) => async dispatch =>{
    const requestOptions = {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get("csrftoken") // this will get cookie
        },
        mode: 'same-origin',
        body: JSON.stringify({ username: username, password: password }),
    };

    try{
        
        fetch('/api/login', requestOptions)
        .then( response => {
            if(response.status >= 200 && response.status <= 299){
                dispatch({ type: LOGIN_SUCCESS })
                dispatch(load_user());
                dispatch(load_product());
            }else{
                return response.json()
            }
        }).then( data => {
            const errors = data.error
            for( const key in errors){
                if(errors.hasOwnProperty(key)){
                    dispatch({ 
                        type: LOGIN_FAIL,
                        payload: errors[key][0]
                    })
                }
            }
        })

    }
    catch(err) {
        dispatch({ 
            type: LOGIN_FAIL  
        })
    }
}


export const register = (username, password, re_password) => async dispatch => {

}


export const logout = () => async dispatch => {
    const requestOptions = {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get("csrftoken") // this will get cookie
        },
        mode: 'same-origin',
        body: JSON.stringify({ 'withCredentials': true }),
    };

    try{

        await fetch('/api/logout', requestOptions)
        .then( res => {
            if(data.status >= 200 && data.status <= 299){
                dispatch({ type: LOGOUT_SUCCESS });
            }else{
                dispatch({ type: LOGOUT_FAIL });
            }
        })

    }catch(err){
        dispatch({ type: LOGOUT_FAIL });
    }
}

export const delete_account = () => async dispatch => {

}