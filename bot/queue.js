// make sure we use the Heroku Redis URL
// (put REDIS_URL=redis://localhost:6379 in .env for local testing)

var kue = require('kue'), queue = kue.createQueue({
    redis: process.env.REDIS_URL,
    prefix: `melk_bot_${process.env.NODE_ENV}`
  });
  
module.exports = queue;