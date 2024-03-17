import {
    CREATE_PRODUCT_SUCCESS,
    CREATE_PRODUCT_FAIL,
    LOAD_PRODUCTS_SUCCESS,
    LOAD_PRODUCTS_FAIL,
    UPDATE_PRODUCT_SUCCESS,
    UPDATE_PRODUCT_FAIL,
    DELETE_PRODUCT_SUCCESS,
    DELETE_PRODUCT_FAIL 

} from '../actions/types';

const initialState = {
    product: "",
}

export default function(state = initialState, action) {
    const { type, payload } = action

    switch(type) { 
        case CREATE_PRODUCT_SUCCESS:
        case CREATE_PRODUCT_FAIL:
        case LOAD_PRODUCTS_SUCCESS:
            return {
                ...state,
                product: payload,
            }
        case LOAD_PRODUCTS_FAIL:
            return {
                ...state,
                product: "",
            }
        case UPDATE_PRODUCT_SUCCESS:
        case UPDATE_PRODUCT_FAIL:
        case DELETE_PRODUCT_SUCCESS:
        case DELETE_PRODUCT_FAIL:
        default:
            return state
    }
}