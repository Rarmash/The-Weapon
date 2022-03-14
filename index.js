const { Client, MessageEmbed } = require('discord.js');
const client = new Client({ partials: ['MESSAGE'] });

client.login('OTM1NTYwOTY4Nzc4NDQ4OTQ3.YfAbDA.0HTrBBZrFaHuOs3gWSNtZQs5dl8');

client.on('ready', () => {
    console.log(`${client.user.tag} logged in.`);
    client.user.setActivity('за ореолом Дзета', { 
        type: 'WATCHING',
        url: 'https://www.twitch.tv/halo' 
    })
		  .then(presence => console.log(`Activity set to ${presence.activities[0].name}`))
		  .catch(console.error);
});

client.on('messageDelete', message => {
    if(!message.partial) {
        const channel = client.channels.cache.get('952519133117960192');
        if((channel) && ((message.channel.id != '647756597904408617') && (message.channel.id != '952519133117960192'))) {
            const embed = new MessageEmbed()
                .setTitle('Удалённое сообщение')
                .setColor('#209af8')
                .addField('Автор', `<@${message.author.id}>`, true)
                .addField('Канал', `<#${message.channel.id}>`, true)
                .setDescription(message.content)
                .setTimestamp();
            channel.send(embed);
        }
    }
}); 