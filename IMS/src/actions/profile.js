import Cookies from 'js-cookie';
import {
    LOAD_USER_PROFILE_SUCCESS,
    LOAD_USER_PROFILE_FAIL,
    UPDATE_USER_PROFILE_SUCCESS,
    UPDATE_USER_PROFILE_FAIL
} from './types';


export const load_user = () => async dispatch =>  {
    const requestOptions = {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json"
        }
    };

    try{
        await fetch('/api/profile', requestOptions)
        .then( res => {
            if (res.status >= 200 && res.status <= 299) { return res.json()  } 
            
        })
        .then( data => {
            dispatch({ 
                type: LOAD_USER_PROFILE_SUCCESS,
                payload: data
            })
        })
        .catch( err => { dispatch({ type: LOAD_USER_PROFILE_FAIL }) })
        .done();
    }catch (err){
        dispatch({ type: LOAD_USER_PROFILE_FAIL })
    }
}

export const update_profile = (first_name, last_name, address) => async dispatch => {

}