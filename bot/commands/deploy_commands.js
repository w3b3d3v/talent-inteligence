const { REST, SlashCommandBuilder, Routes } = require('discord.js');
const { client_id,  bot_token, guild_id } = require('../../config/auth.json');

const commands = [
	new SlashCommandBuilder()
    .setName('get').setDescription('get')
    .addStringOption(option => option.setName('input').setDescription('Channel Id')),

    new SlashCommandBuilder().setName('process').setDescription('process')
]
	.map(command => command.toJSON());

const rest = new REST({ version: '10' }).setToken(bot_token);

rest.put(Routes.applicationGuildCommands(client_id, guild_id), { body: commands })
	.then((data) => console.log(`Successfully registered ${data.length} application commands.`))
	.catch(console.error);

    