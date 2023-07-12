import axios from 'axios';

import logger from 'src/utils/logger';
import Auth from './auth';
import Result from './result';
import ScanRequest from './scanRequest';
import Task from './task';
import Vulnerability from './vulnerability';

export const axiosInstance = axios.create({
  baseURL: process.env.API_URL,
  headers: {},
  withCredentials: true,
});

axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.request && error.request.status === 401) {
      // Set Failed Request
      let failedRequest = error.config;
      logger.debug('Authentication Failed!');
      throw error; // if needed can return error instead of throwing the error
      // TODO: Handle failed authentication

      // //Method to get new token
      // return renewUserToken().then((response) => {
      //   // Set axios instance header
      //   axiosInstance.defaults.headers['Authorization'] = 'Bearer ' + response.token;

      //   // Set failed request header
      //   failedRequest.headers['Authorization'] = 'Bearer ' + response.token;

      //   //Retry failed request
      //   return axios.request(failedRequest);
      // });
    }
    throw error;
  }
);

export const api = {
  ...Auth(axiosInstance),
  ...ScanRequest(axiosInstance),
  ...Task(axiosInstance),
  ...Result(axiosInstance),
  ...Vulnerability(axiosInstance),
};

export default api;
