var AuthConfig = {};
try {
  AuthConfig = require("../config/auth.json");
} catch (e) { }

if (!AuthConfig.hasOwnProperty('bot_token')) {
  //attempt to populate from ENV variables. useful for remote cloud deploys
  AuthConfig = {
    bot_token: process.env.BOT_TOKEN,
    client_id: process.env.BOT_CLIENT_ID,
    guild_id: process.env.GUILD_ID
  }
}

if (!AuthConfig.hasOwnProperty("bot_token") || AuthConfig.bot_token === "") {
  console.error(
    "Please create an config/auth.json or specify environmental variables, the bot cannot run without a bot_token"
  ); // send message for error - no token
  process.exit();
}

module.exports = AuthConfig