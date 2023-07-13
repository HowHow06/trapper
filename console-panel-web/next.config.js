const nextConfig = {
  // output: 'standalone',
  reactStrictMode: true,
  env: {
    API_URL: process.env.API_URL, // need to declare for them to work at client side
  },
};

module.exports = nextConfig;
