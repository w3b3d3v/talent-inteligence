require('dotenv').config()
const bot = require('./bot/client')
const fs = require("fs");

bot.on("ready", async function () {
    console.log("working bot!")
});