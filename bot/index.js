// Require the necessary discord.js classes
const { Client, GatewayIntentBits } = require('discord.js');
const { bot_token } = require('../config/auth.json');

// Create a new client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

// When the client is ready, run this code (only once)
client.once('ready', () => {
	console.log('Ready!');
});

client.on('interactionCreate', async interaction => {
	if (!interaction.isChatInputCommand()) return;

	const { commandName } = interaction;
    channelId = interaction.options.getString('input');
	if (commandName == 'get') {
        console.log(client.channels.cache.find(channel=> channel.id == channelId))
		await interaction.reply('Pong!');
	} else {
        return;
    }
});

// Login to Discord with your client's token
client.login(bot_token);
