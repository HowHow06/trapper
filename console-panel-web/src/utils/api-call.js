export const apiCall = async ({ axiosInstance, url, params = null, options = {} }) => {
  try {
    const response = params
      ? await axiosInstance.post(url, params, options)
      : await axiosInstance.post(url, options);
    return { success: true, ...response };
  } catch (error) {
    return { success: false, error: error };
  }
};

export const isApiSuccess = (response) => {
  return response.status >= 200 && response.status < 300 && response.success;
};

export const getErrorMessageFromResponse = (response) => {
  const errorObject = response.error;
  return errorObject.response?.data?.detail ?? errorObject.message;
};
