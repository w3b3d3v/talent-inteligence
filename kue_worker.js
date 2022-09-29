var kue = require('kue')
  , url = require('url')
  , redis = require('redis')
  , kue_jobs = require('./bot/queue');

var jobs = {}
var normalizedPath = require("path").join(__dirname, "bot", "jobs");

var jobCount = 0;
require("fs")
  .readdirSync(normalizedPath)
  .filter(file => {
    return (file.indexOf('.') !== 0) && (file.slice(-3) === '.js');
  })
  .forEach(function (file) {
    var job = require("./bot/jobs/" + file);
    jobs[job.queue_name] = job
    jobCount++;
  });

console.log("Loaded " + jobCount + " job(s)")

if (process.env.BOT_DISABLED == 'true') {
  console.log('BOT is disabled on this environment.')
} else {
  for (const jobKey in jobs) {
    kue_jobs.process(jobs[jobKey].queue_name, jobs[jobKey].perform);
  }
}