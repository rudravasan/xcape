import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import json
from discord.ext import commands

token = 'MTIxODIzMDc5MjIxNjY0MTU4Ng.G23oBZ.WtmIHIL-4wKHDH7ufTMYmWUTaoLdYKazntNAJA'

prefix = '!'
intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', intents=intents, help_command=None)


@client.event
async def on_ready():
    print(f'{client.user} is online and ready to use')
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=f'{prefix}help | DEV BY RUDRA'))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(f'I can\'t find this command\ntype {prefix}help to get help')

@client.command()
async def utility(ctx):
    embed = discord.Embed(colour=0xc8dc6c)
    embed.add_field(name=f"{prefix}ping", value="bot ping")
    embed.add_field(name=f"{prefix}invite", value="Invite me in your server")
    embed.add_field(name=f"{prefix}afk", value="set afk")
    embed.add_field(name=f"{prefix}av", value="see your/others avatar")
    embed.add_field(name=f"{prefix}userinfo", value="get userinfo")
    await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    embed = discord.Embed(colour=0xc8dc6c)
    embed.add_field(name=f"{prefix}utility", value="utility commands")
    embed.add_field(name=f"{prefix}moderation", value="moderation commands")
    embed.add_field(name=f"{prefix}welcomer", value="welcome commands")
    await ctx.send(embed=embed)

@client.command()
async def moderation(ctx):
    embed = discord.Embed(colour=0xc8dc6c)
    embed.add_field(name=f"{prefix}ban", value="ban member")
    embed.add_field(name=f"{prefix}kick", value="kick member")
    embed.add_field(name=f"{prefix}mute", value="mute member")
    embed.add_field(name=f"{prefix}unmute", value="unmute member")
    embed.add_field(name=f"{prefix}purge", value="purge messages")
    await ctx.send(embed=embed)    

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
    await ctx.reply(
      f'I can\'t find this command\ntype {prefix}help to get help')
    

@client.command()
async def ping(ctx):
  await ctx.reply("pong")

@client.command()
async def invite(ctx):
  await ctx.reply("[Click here to invite me](https://discord.com/oauth2/authorize?client_id=1218230792216641586&permissions=8&scope=bot)")

@client.command()
async def dmuser(ctx, member: discord.Member, *, message):
    try:
        await member.send(message)
        await ctx.send(f"Direct message sent to {member.mention}")
    except discord.Forbidden:
        await ctx.send("Could not send a direct message to this user. Please make sure your DMs are open.")

@client.command()
async def purge(ctx, amount: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"{amount} messages deleted.", delete_after=5)
    else:
        await ctx.send("You do not have the permissions to manage messages.")

@client.command()
async def mute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        # Check if the Muted role exists, if not, create it
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)

        # Add the Muted role to the member
        await member.add_roles(muted_role)
        await ctx.send(f"{member.mention} has been muted.")
    else:
        await ctx.send("You do not have the permissions to manage roles.")

@client.command()
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f"{member.mention} has been unmuted.")
    else:
        await ctx.send(f"{member.mention} is not muted.")
@client.command()
async def setwelcome(ctx, channel: discord.TextChannel, *, message):
    print("Set welcome command executed.")  # Debug print

    # Check if the user has the necessary permissions to configure the welcome message
    if ctx.author.guild_permissions.manage_channels:
        # Open the JSON file where the welcome messages are stored
        try:
            with open("welcome_messages.json", "r") as file:
                welcome_messages = json.load(file)
        except FileNotFoundError:
            welcome_messages = {}

        # Update or add the welcome message for the specified channel
        welcome_messages[str(ctx.guild.id)] = {"channel_id": channel.id, "message": message}

        # Debug print to check the contents of welcome_messages
        print("Updated welcome messages:", welcome_messages)

        # Save the updated welcome messages to the JSON file
        try:
            with open("welcome_messages.json", "w") as file:
                json.dump(welcome_messages, file, indent=4)
        except Exception as e:
            print("Error saving welcome message to JSON file:", e)  # Debug print
            await ctx.send("An error occurred while saving the welcome message.")

        await ctx.send(f"Welcome message set for {channel.mention}.")
    else:
        await ctx.send("You do not have the permissions to manage channels.")
@client.event
async def on_member_join(member):
    try:
        with open("welcome_messages.json", "r") as file:
            welcome_messages = json.load(file)
    except FileNotFoundError:
        welcome_messages = {}

    if str(member.guild.id) in welcome_messages:
        welcome_data = welcome_messages[str(member.guild.id)]
        channel = member.guild.get_channel(welcome_data["channel_id"])
        message = welcome_data["message"]

        embed = discord.Embed(title="Welcome", description=message.format(member=member.mention), color=discord.Color.green())
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)
    else:
        # Default welcome message if not set
        default_message = f"Welcome to the server, {member.mention}!"
        embed = discord.Embed(title="Welcome", description=default_message, color=discord.Color.green())
        embed.set_thumbnail(url=member.avatar_url)
        await member.guild.system_channel.send(embed=embed)
@client.command()
async def testwelcome(ctx):
    try:
        with open("welcome_messages.json", "r") as file:
            welcome_messages = json.load(file)
    except FileNotFoundError:
        await ctx.send("Welcome messages have not been set up yet.")
        return

    if str(ctx.guild.id) in welcome_messages:
        welcome_data = welcome_messages[str(ctx.guild.id)]
        channel = ctx.guild.get_channel(welcome_data["channel_id"])
        message = welcome_data["message"]
        await channel.send(message.format(member=ctx.author.mention))
        await ctx.send("Test welcome message sent.")
    else:
        await ctx.send("Welcome message has not been set up for this server.")


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members:
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} has been banned.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to ban members.")
    else:
        await ctx.send("You do not have the permissions to ban members.")

@client.command()
async def unban(ctx, *, member):
    if ctx.author.guild_permissions.ban_members:
        banned_users = await ctx.guild.bans()

        # Split the member argument into name and discriminator
        try:
            member_name, member_discriminator = member.split('#')
        except ValueError:
            await ctx.send("Invalid format. Please provide the banned user's name and discriminator (username#discriminator).")
            return

        # Check if the banned user is in the ban list
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.name}#{user.discriminator} has been unbanned.")
                return

        await ctx.send(f"{member_name}#{member_discriminator} is not in the ban list.")
    else:
        await ctx.send("You do not have the permissions to unban members.")

@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
          if ctx.author.guild_permissions.kick_members:
              await member.kick(reason=reason)
              await ctx.send(f"{member.mention} has been kicked.")
          else:
              await ctx.send("You do not have the permissions to kick members.")
@client.command()
async def av(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Avatar of {member.display_name}", color=discord.Color.blue())
    await ctx.send(embed=embed)

@client.command()
async def welcomer(ctx):
  embed = discord.Embed(colour=0xc8dc6c)
  embed.add_field(name=f"{prefix}setwelcome", value="type !setwelcome [channel id] {member} then your message ")
  embed.add_field(name=f"{prefix}welcometest", value="test your welcome message")



  await ctx.send(embed=embed)

trigger_messages = {}  # Dictionary to store trigger messages

@client.command()
async def trigger(ctx, trigger_word, *, message):
    trigger_messages[trigger_word.lower()] = message
    await ctx.send(f'Trigger message set for "{trigger_word}".')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    for trigger_word, response in trigger_messages.items():
        if trigger_word in content:
            await message.channel.send(response)

    await client.process_commands(message)


# Dictionary to store user XP and levels for each server
server_levels = {}

@client.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore messages from bots

    server_id = message.guild.id

    # Check if the server has set a level up channel
    if server_id in server_levels and message.channel.id == server_levels[server_id]:
        # Check if the user is already in the server's level_ups dictionary
        if message.author.id not in server_levels[server_id]["level_ups"]:
            server_levels[server_id]["level_ups"][message.author.id] = {"xp": 0, "level": 1}

        # Add XP for each message
        server_levels[server_id]["level_ups"][message.author.id]["xp"] += 5

        # Level up if XP reaches a certain threshold
        if server_levels[server_id]["level_ups"][message.author.id]["xp"] >= 100:
            server_levels[server_id]["level_ups"][message.author.id]["level"] += 1
            server_levels[server_id]["level_ups"][message.author.id]["xp"] = 0
            level_up_channel = client.get_channel(server_levels[server_id]["channel_id"])
            await level_up_channel.send(f"🎉 Congratulations, {message.author.mention}! You've leveled up to level {server_levels[server_id]['level_ups'][message.author.id]['level']}!")

    await client.process_commands(message)

@client.command()
async def set_levelup_channel(ctx, channel: discord.TextChannel):
    # Check if the user has permissions to set the level up channel
    if ctx.author.guild_permissions.administrator:
        server_id = ctx.guild.id
        if server_id not in server_levels:
            server_levels[server_id] = {"channel_id": None, "level_ups": {}}
        server_levels[server_id]["channel_id"] = channel.id
        await ctx.send(f"Level up channel set to {channel.mention} for this server.")
    else:
        await ctx.send("You do not have permission to set the level up channel.")

@client.command()
async def rank(ctx, member: discord.Member = None):
    member = member or ctx.author
    server_id = ctx.guild.id
    if server_id in server_levels and member.id in server_levels[server_id]["level_ups"]:
        embed = discord.Embed(title=f"Rank for {member.display_name}", color=discord.Color.gold())
        embed.add_field(name="Level", value=server_levels[server_id]["level_ups"][member.id]["level"], inline=True)
        embed.add_field(name="XP", value=server_levels[server_id]["level_ups"][member.id]["xp"], inline=True)
        await ctx.send(embed=embed)
    else:
        await ctx.send("User not found in the level system or level up channel is not set for this server.")


afk_users = {}

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Check if the author is mentioned and if they are AFK
    for user_id, data in afk_users.items():
        if f"<@{user_id}>" in message.content:
            embed = discord.Embed(title="AFK Status", description=f"{message.author.mention}, {message.guild.get_member(user_id)} is currently AFK: {data['message']}", color=discord.Color.orange())
            await message.channel.send(embed=embed)

    # Remove AFK status if the author was AFK and sent a message
    if message.author.id in afk_users:
        del afk_users[message.author.id]
        embed = discord.Embed(title="AFK Removed", description=f"Welcome back, {message.author.mention}! Your AFK status has been removed.", color=discord.Color.green())
        await message.channel.send(embed=embed)

    await client.process_commands(message)
@client.command()
async def userinfo(ctx, member: discord.Member = None):
    """
    Display information about the specified user or the user invoking the command.
    """
    try:
        if member is None:
            member = ctx.author

        embed = discord.Embed(title="User Information", color=discord.Color.blue())

        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="Discriminator", value=member.discriminator, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Joined Discord", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)

        await ctx.send(embed=embed)
    except Exception as e:
        print(e)  # Print the exception to the console for debugging
        await ctx.send("An error occurred while processing the command.")

client.run(token)
