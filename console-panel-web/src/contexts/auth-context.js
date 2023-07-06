import PropTypes from 'prop-types';
import { createContext, useContext, useEffect, useReducer, useRef } from 'react';
import { DEFAULT } from 'src/constants/variables';
import { isApiSuccess } from 'src/utils/api-call';
import logger from 'src/utils/logger';
import api from '../api';

const HANDLERS_ACTION_TYPES = {
  INITIALIZE: 'INITIALIZE',
  SIGN_IN: 'SIGN_IN',
  SIGN_OUT: 'SIGN_OUT',
};

const initialState = {
  isAuthenticated: false,
  isLoading: true,
  user: null,
};

const handlers = {
  [HANDLERS_ACTION_TYPES.INITIALIZE]: (state, action) => {
    const user = action.payload;

    return {
      ...state,
      ...// if payload (user) is provided, then is authenticated
      (user
        ? {
            isAuthenticated: true,
            isLoading: false,
            user,
          }
        : {
            isLoading: false,
          }),
    };
  },
  [HANDLERS_ACTION_TYPES.SIGN_IN]: (state, action) => {
    const user = action.payload;

    return {
      ...state,
      isAuthenticated: true,
      user,
    };
  },
  [HANDLERS_ACTION_TYPES.SIGN_OUT]: (state) => {
    return {
      ...state,
      isAuthenticated: false,
      user: null,
    };
  },
};

const reducer = (state, action) => {
  return handlers[action.type] ? handlers[action.type](state, action) : state;
};

// The role of this context is to propagate authentication state through the App tree.

// initially is undefined, see AuthContext.Provider below to see the value
export const AuthContext = createContext({ undefined });

export const AuthProvider = (props) => {
  const { children } = props;
  const [state, dispatch] = useReducer(reducer, initialState);
  const initialized = useRef(false);
  logger.debug('user state from auth-context:', state?.user);

  const initialize = async () => {
    // Prevent from calling twice in development mode with React.StrictMode enabled
    if (initialized.current) {
      return;
    }

    initialized.current = true;
    let isAuthenticated = false;

    const response = await api.testToken();
    if (isApiSuccess(response)) {
      logger.debug('Legit User!', response.data);
      isAuthenticated = true;
    } else {
      logger.debug('Test Token failed', response.error);
    }

    if (isAuthenticated) {
      const userInfo = response.data;
      const user = {
        id: userInfo.id,
        avatar: DEFAULT.AVATAR,
        username: userInfo.username,
        email: userInfo.email,
        isActive: userInfo.is_active,
        isAdmin: userInfo.is_admin,
      };

      dispatch({
        type: HANDLERS_ACTION_TYPES.INITIALIZE,
        payload: user,
      });
    } else {
      dispatch({
        type: HANDLERS_ACTION_TYPES.INITIALIZE,
      });
    }
  };

  useEffect(
    () => {
      initialize();
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  const signIn = async (username, password) => {
    let response = await api.login({
      username,
      password,
    });

    if (isApiSuccess(response)) {
      logger.debug('Login succeeded', response.data);
    } else {
      logger.debug('Login failed', response.error);
      return response;
    }

    response = await api.testToken();
    if (!isApiSuccess(response)) {
      logger.debug('Login Token failed', response.error);
      return response;
    }

    const userInfo = response.data;

    const user = {
      id: userInfo.id,
      avatar: DEFAULT.AVATAR,
      username: userInfo.username,
      email: userInfo.email,
      isActive: userInfo.is_active,
      isAdmin: userInfo.is_admin,
    };

    dispatch({
      type: HANDLERS_ACTION_TYPES.SIGN_IN,
      payload: user,
    });

    return response;
  };

  const signUp = async (email, name, password) => {
    throw new Error('Sign up is not implemented');
  };

  const signOut = async () => {
    const response = await api.logout();

    if (isApiSuccess(response)) {
      // Successful response
      logger.debug('Logout succeeded', response.data);
    } else {
      logger.debug('Logout failed', response.error);
      return;
    }

    dispatch({
      type: HANDLERS_ACTION_TYPES.SIGN_OUT,
    });
  };

  return (
    <AuthContext.Provider
      value={{
        ...state,
        signIn,
        signUp,
        signOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

AuthProvider.propTypes = {
  children: PropTypes.node,
};

export const AuthConsumer = AuthContext.Consumer;

export const useAuthContext = () => useContext(AuthContext);
