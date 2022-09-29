let Discord;
try {
  Discord = require("discord.js");
} catch (e) {
  console.log(e.stack);
  console.log(process.version);
  console.log("Please run npm install and ensure it passes with no errors!"); // if there is an error, tell to install dependencies.
  process.exit();
}

console.log(
  "Starting DiscordBot\nNode version: " +
  process.version +
  "\nDiscord.js version: " +
  Discord.version
); // send message notifying bot boot-up

const discord_client = new Discord.Client({
  intents: [
    Discord.GatewayIntentBits.Guilds,
    Discord.GatewayIntentBits.GuildMessages,
    Discord.GatewayIntentBits.GuildMessageReactions,
    Discord.GatewayIntentBits.DirectMessages,
    Discord.GatewayIntentBits.DirectMessageReactions
  ]
});

var AuthDetails = require("./auth.js");
if (AuthDetails.bot_token) {
  console.log("logging in with token");
  discord_client.login(AuthDetails.bot_token);
} else {
  console.log(
    "Logging in with user credentials is no longer supported!\nYou can use token based log in with a user account; see\nhttps://discord.js.org/#/docs/main/master/general/updating."
  );
}

module.exports = discord_client;