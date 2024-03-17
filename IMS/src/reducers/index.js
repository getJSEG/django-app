import { combineReducers } from 'redux';
import auth from './auth';
import profile from './profile';
import products from './products';
import varients from './varients';

export default combineReducers({
    auth,
    profile,
    products,
    varients
});