import { apiCall } from 'src/utils/api-call';

export default function Auth(api) {
  const login = async ({ username, password }) => {
    // this login api uses HTTP-only cookie, cookie will be set automatically when the response reaches the browser
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    return await apiCall({
      axiosInstance: api,
      url: `/auth/login`,
      params,
    });
  };

  const register = async ({ username, email, password }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/auth/register`,
      params: {
        username: username,
        email: email,
        password: password,
      },
    });
  };

  const editPassword = async ({ oldPassword, newPassword }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/auth/edit-password`,
      method: `put`,
      params: {
        old_password: oldPassword,
        new_password: newPassword,
      },
    });
  };

  const testToken = async () => {
    return await apiCall({ axiosInstance: api, url: `/auth/test-token` });
  };

  const logout = async () => {
    return await apiCall({ axiosInstance: api, url: `/auth/logout` });
  };

  const forgotPassword = async ({ email }) => {
    return await apiCall({ axiosInstance: api, url: `/auth/password-recovery/${email}` });
  };

  const resetPassword = async ({ token, password }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/auth/reset-password`,
      params: {
        token: token,
        new_password: password,
      },
    });
  };

  return {
    login,
    testToken,
    logout,
    register,
    editPassword,
    forgotPassword,
    resetPassword,
  };
}
