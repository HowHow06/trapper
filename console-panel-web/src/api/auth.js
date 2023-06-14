import { apiCall } from 'src/utils/api-call';

export default function Auth(api) {
  const login = async ({ username, password }) => {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    return await apiCall({
      axiosInstance: api,
      url: `/auth/login`,
      params,
    });
  };

  const testToken = async () => {
    return await apiCall({ axiosInstance: api, url: `/auth/test-token` });
  };

  const logout = async () => {
    return await apiCall({ axiosInstance: api, url: `/auth/logout` });
  };

  return {
    login,
    testToken,
    logout,
  };
}
