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
    product: null,
    loading: true,
    productCreated: false

}

export default function(state = initialState, action) {
    const { type, payload } = action

    switch(type) { 
        case CREATE_PRODUCT_SUCCESS:
            return {
                ...state,
                productCreated: payload,
                loading: false
            }
        case CREATE_PRODUCT_FAIL:
            return {
                ...state,
                productCreated: payload,
                loading: true
            }
        case LOAD_PRODUCTS_SUCCESS:
            return {
                ...state,
                product: payload,
                loading: false
            }
        case LOAD_PRODUCTS_FAIL:
            return {
                ...state,
                product: "",
                loading: true
            }
        case UPDATE_PRODUCT_SUCCESS:
        case UPDATE_PRODUCT_FAIL:
        case DELETE_PRODUCT_SUCCESS:
        case DELETE_PRODUCT_FAIL:
        default:
            return state
    }
}