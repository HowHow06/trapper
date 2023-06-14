const logger = {
  log: console.log,
  debug: (message, ...optionalParams) => {
    if (process.env.NODE_ENV == 'development') {
      console.log(message, ...optionalParams);
    }
  },
};
export default logger;
