
// Require the necessary discord.js classes
const { Client, GatewayIntentBits } = require('discord.js');
const { bot_token } = require('../config/auth.json');

// Create a new client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

// When the client is ready, run this code (only once)
client.once('ready', () => {
	console.log('Ready!');
});

client.on('interactionCreate', async interaction => {
	if (!interaction.isChatInputCommand()) return;
    
	const { commandName } = interaction;

	if (commandName == 'get') {
        channelId = interaction.options.getString('input');
    
        if(channelId.match(/^[0-9]*/)[0] == '') {
            console.log('This is not a channel Id.')
            await interaction.reply('This is not a channel Id.');
            return;
        }

        try {
            let msgs = []
            let ids = []
            const job = require('./jobs/processJob');
            channel = client.channels.cache.find(channel=> channel.id == channelId);
            let messages = await channel.messages.fetch();
            messages = Array.from(messages.values())
            
            messages.forEach(message => {  
                ids.push(message.author.id)
                msgs.push(message.content)
            })
            
            await job.storeMessages(msgs, ids)
		    await interaction.reply({content: 'Messages stored', ephemeral: true});
        }
        catch(e) {
            console.error(e);
            await interaction.reply('Algo deu errado.');
        }
	} 
    
    else {
        return;
    }
});

// Login to Discord with your client's token
client.login(bot_token);
