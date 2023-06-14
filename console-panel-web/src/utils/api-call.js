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
