import { apiCall } from '../utils/api-call'

export default function Auth(api) {
  const testToken = async () => {
    return await apiCall({ axiosInstance: api, url: `/auth/test-token` })
  }

  return {
    testToken,
  }
}
