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
} from '../actions/types';

const initialState = {
    isAuthenticated: null,
    loading: true,
    fieldErr:"",
};

export default function(state = initialState, action) {
    const { type, payload } = action;

    switch(type) {
        case AUTHENTICATED_SUCCESS:
        case AUTHENTICATED_FAIL:
            return {
                ...state,
                isAuthenticated: payload,
                loading: false
            }
        case REGISTER_SUCCESS:
            return {
                ...state,
                isAuthenticated: false,
                loading: false,
                loading: true
            }
        case LOGIN_SUCCESS:
            return {
                ...state,
                isAuthenticated: true,
                fieldErr:"",
            }
        case LOGOUT_SUCCESS:
        case DELETE_USER_SUCCESS:
            return {
                ...state,
                isAuthenticated: false
            }
        case REGISTER_FAIL:
        case LOGIN_FAIL:
            return {
                ...state,
                fieldErr: payload
            }
        case LOGOUT_FAIL:
            return {
                ...state,
                loading: false
            }
        case DELETE_USER_FAIL:
            return state
        default:
            return state
    };
};