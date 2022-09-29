// Require the necessary discord.js classes
const { Client, GatewayIntentBits } = require('discord.js');
const { bot_token } = require('../config/auth.json');

// Create a new client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });
const messages = [];

// When the client is ready, run this code (only once)
client.once('ready', () => {
	console.log('Ready!');
});

client.on('interactionCreate', async interaction => {
	if (!interaction.isChatInputCommand()) return;

	const { commandName } = interaction;
    channelId = interaction.options.getString('input');
	if (commandName == 'get') {
        channel = client.channels.cache.find(channel=> channel.id == channelId);
        channel.messages.fetch().then(messages => {
            messages.forEach(message => messages.append(message.content))
        })
		await interaction.reply('Pong!');
	} else {
        return;
    }
});

// Login to Discord with your client's token
client.login(bot_token);
