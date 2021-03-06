import discord
import typing
from redbot.core import commands
from typing import List
from dislash import ActionRow, Button, ButtonStyle
from .utils import utils

class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.admin_or_permissions(administrator=True)
    @commands.group(name="setticket", aliases=["ticketset"])
    async def config(self, ctx):
        """Configure TicketTool for your server."""

    @config.command(name="enable", usage="<true_or_false>")
    async def enable(self, ctx, state: bool):
        """Enable or disable Ticket System

        Use `True` (Or `yes`) to enable or `False` (or `no`) to disable.
        """
        config = await self.data.guild(ctx.guild).settings.all()

        if config["category_open"] is None or config["category_close"] is None or config["admin_role"] is None:
            await ctx.send("You cannot enable the ticket system on this server if you have not configured the following options:",
                            f"- The category of open tickets : `{ctx.prefix}setticket categoryopen <category>`",
                            f"- The category of close tickets : `{ctx.prefix}setticket categoryclose <category>`",
                            f"- The admin role has full access to the tickets : `{ctx.prefix}setticket adminrole <role>`",
                            "All other parameters are optional or have default values that will be used.")

        actual_enable = config["enable"]
        if actual_enable is state:
            await ctx.send(f"Ticket System is already set on {state}.")
            return

        await self.data.guild(ctx.guild).settings.enable.set(state)
        await ctx.send(f"Ticket System state registered: {state}.")

    @config.command(aliases=["lchann", "lchannel", "logschan", "logchannel", "logsc"], usage="<text_channel_or_'none'>")
    async def logschannel(self, ctx, *, channel: typing.Optional[discord.TextChannel]=None):
        """Set a channel where events are registered.

        ``channel``: Text channel.
        You can also use "None" if you wish to remove the logging channel.
        """
        if channel is None:
            await self.data.guild(ctx.guild).settings.logschannel.clear()
            await ctx.send("Logging channel removed.")
            return

        needperm = await self.check_permissions_in_channel(["embed_links", "read_messages", "read_message_history", "send_messages", "attach_files"], channel)
        if needperm:
            await ctx.send("The bot does not have at least one of the following permissions in this channel: `embed_links`, `read_messages`, `read_message_history`, `send_messages`, `attach_files`.")
            return

        await self.data.guild(ctx.guild).settings.logschannel.set(channel.id)
        await ctx.send(f"Logging channel registered: {channel.mention}.")

    @config.command(usage="<category_or_'none'>")
    async def categoryopen(self, ctx, *, category: typing.Optional[discord.CategoryChannel]=None):
        """Set a category where open tickets are created.

        ``category``: Category.
        You can also use "None" if you wish to remove the open category.
        """
        if category is None:
            await self.data.guild(ctx.guild).settings.category_open.clear()
            await ctx.send("Category Open removed.")
            return

        await self.data.guild(ctx.guild).settings.category_open.set(category.id)
        await ctx.send(f"Category Open registered: {category.name}.")

    @config.command(usage="<category_or_'none'>")
    async def categoryclose(self, ctx, *, category: typing.Optional[discord.CategoryChannel]=None):
        """Set a category where close tickets are created.

        ``category``: Category.
        You can also use "None" if you wish to remove the close category.
        """
        if category is None:
            await self.data.guild(ctx.guild).settings.category_close.clear()
            await ctx.send("Category Close removed.")
            return

        await self.data.guild(ctx.guild).settings.category_close.set(category.id)
        await ctx.send(f"Category Close registered: {category.name}.")

    @config.command(usage="<role_or_'none'>")
    async def adminrole(self, ctx, *, role: typing.Optional[discord.Role]=None):
        """Set a role for administrators of the ticket system.

        ``role``: Role.
        You can also use "None" if you wish to remove the admin role.
        """
        if role is None:
            await self.data.guild(ctx.guild).settings.admin_role.clear()
            await ctx.send("Admin Role removed.")
            return

        await self.data.guild(ctx.guild).settings.admin_role.set(role.id)
        await ctx.send(f"Admin Role registered: {role.name}.")

    @config.command(usage="<role_or_'none'>")
    async def supportrole(self, ctx, *, role: typing.Optional[discord.Role]=None):
        """Set a role for helpers of the ticket system.

        ``role``: Role.
        You can also use "None" if you wish to remove the support role.
        """
        if role is None:
            await self.data.guild(ctx.guild).settings.support_role.clear()
            await ctx.send("Support Role removed.")
            return

        await self.data.guild(ctx.guild).settings.support_role.set(role.id)
        await ctx.send(f"Support Role registered: {role.name}.")

    @config.command(usage="<role_or_'none'>")
    async def ticketrole(self, ctx, *, role: typing.Optional[discord.Role]=None):
        """Set a role for creaters of a ticket.

        ``role``: Role.
        You can also use "None" if you wish to remove the ticket role.
        """
        if role is None:
            await self.data.guild(ctx.guild).settings.ticket_role.clear()
            await ctx.send("Ticket Role removed.")
            return

        await self.data.guild(ctx.guild).settings.ticket_role.set(role.id)
        await ctx.send(f"Ticket Role registered: {role.name}.")

    @config.command(usage="<role_or_'none'>")
    async def viewrole(self, ctx, *, role: typing.Optional[discord.Role]=None):
        """Set a role for viewers of tickets.

        ``role``: Role.
        You can also use "None" if you wish to remove the view role.
        """
        if role is None:
            await self.data.guild(ctx.guild).settings.view_role.clear()
            await ctx.send("View Role removed.")
            return

        await self.data.guild(ctx.guild).settings.view_role.set(role.id)
        await ctx.send(f"View Role registered: {role.name}.")

    @config.command(usage="<role_or_'none'>")
    async def pingrole(self, ctx, *, role: typing.Optional[discord.Role]=None):
        """Set a role for pings on ticket creation.

        ``role``: Role.
        You can also use "None" if you wish to remove the ping role.
        """
        if role is None:
            await self.data.guild(ctx.guild).settings.ping_role.clear()
            await ctx.send("Ping Role removed.")
            return

        await self.data.guild(ctx.guild).settings.ping_role.set(role.id)
        await ctx.send(f"Ping Role registered: {role.name}.")

    @config.command(usage="<int>")
    async def nbmax(self, ctx, int: int):
        """Max Number of tickets for a member.
        """
        if int == 0:
            await ctx.send("Disable the system instead.")
            return

        await self.data.guild(ctx.guild).nb_max.set(int)
        await ctx.send(f"Max Number registered: {int}.")

    @config.command(usage="<true_or_false>")
    async def modlog(self, ctx, state: bool):
        """Enable or disable Modlog.

        Use `True` (Or `yes`) to enable or `False` (or `no`) to disable.
        """
        config = await self.data.guild(ctx.guild).settings.all()

        actual_create_modlog = config["create_modlog"]
        if actual_create_modlog is state:
            await ctx.send(f"Modlog is already set on {state}.")
            return

        await self.data.guild(ctx.guild).settings.create_modlog.set(state)
        await ctx.send(f"Modlog state registered: {state}.")

    @config.command(usage="<true_or_false>")
    async def closeonleave(self, ctx, state: bool):
        """Enable or disable Close on Leave.

        Use `True` (Or `yes`) to enable or `False` (or `no`) to disable.
        """
        config = await self.data.guild(ctx.guild).settings.all()

        actual_close_on_leave = config["close_on_leave"]
        if actual_close_on_leave is state:
            await ctx.send(f"Close on Leave is already set on {state}.")
            return

        await self.data.guild(ctx.guild).settings.close_on_leave.set(state)
        await ctx.send(f"Close on Leave state registered: {state}.")

    @config.command(usage="<true_or_false>")
    async def createonreact(self, ctx, state: bool):
        """Enable or disable Create on React ``.

        Use `True` (Or `yes`) to enable or `False` (or `no`) to disable.
        """
        config = await self.data.guild(ctx.guild).settings.all()

        actual_create_on_react = config["create_on_react"]
        if actual_create_on_react is state:
            await ctx.send(f"Create on React is already set on {state}.")
            return

        await self.data.guild(ctx.guild).settings.create_on_react.set(state)
        await ctx.send(f"Create on React state registered: {state}.")




    @config.command(aliases=["colour", "col", "embedcolor", "embedcolour"], usage="<color_or_'none'>")
    async def color(self, ctx, *, color: typing.Optional[discord.Color]=None):
        """Set a colour fort the embed.

        ``color``: Color.
        You can also use "None" if you wish to reset the color.
        """

        if color is None:
            await self.data.guild(ctx.guild).settings.color.clear()
            config = await self.data.guild(ctx.guild).settings.all()
            actual_color = config["color"]
            actual_thumbnail = config["thumbnail"]
            embed: discord.Embed = discord.Embed()
            embed.color = actual_color
            embed.set_thumbnail(url=actual_thumbnail)
            embed.title = "Configure the embed"
            embed.description = "Reset color:"
            embed.add_field(
                name="Color:",
                value=f"{actual_color}")
            message = await ctx.send(embed=embed)
            return

        await self.data.guild(ctx.guild).settings.color.set(color.value)
        config = await self.data.guild(ctx.guild).settings.all()
        actual_color = config["color"]
        actual_thumbnail = config["thumbnail"]
        embed: discord.Embed = discord.Embed()
        embed.title = "Configure the embed"
        embed.description = "Set color:"
        embed.color = actual_color
        embed.set_thumbnail(url=actual_thumbnail)
        embed.add_field(
            name="Color:",
            value=f"{actual_color}")
        message = await ctx.send(embed=embed)

    @config.command(aliases=["picture", "thumb", "link"], usage="<link_or_'none'>")
    async def thumbnail(self, ctx, *, link = None):
        """Set a thumbnail fort the embed.

        ``link``: Thumbnail link.
        You can also use "None" if you wish to reset the thumbnail.
        """

        if link is None:
            await self.data.guild(ctx.guild).settings.thumbnail.clear()
            config = await self.data.guild(ctx.guild).settings.all()
            actual_thumbnail = config["thumbnail"]
            actual_color = config["color"]
            embed: discord.Embed = discord.Embed()
            embed.title = "Configure the embed"
            embed.description = "Reset thumbnail:"
            embed.set_thumbnail(url=actual_thumbnail)
            embed.color = actual_color
            embed.add_field(
                name="Thumbnail:",
                value=f"{actual_thumbnail}")
            message = await ctx.send(embed=embed)
            return

        await self.data.guild(ctx.guild).settings.thumbnail.set(link)
        config = await self.data.guild(ctx.guild).settings.all()
        actual_thumbnail = config["thumbnail"]
        actual_color = config["color"]
        embed: discord.Embed = discord.Embed()
        embed.title = "Configure the embed"
        embed.description = "Set thumbnail:"
        embed.set_thumbnail(url=actual_thumbnail)
        embed.color = actual_color
        embed.add_field(
            name="Thumbnail:",
            value=f"{actual_thumbnail}")
        message = await ctx.send(embed=embed)

    @config.command(name="auditlogs", aliases=["logsaudit"], usage="<true_or_false>")
    async def showauthor(self, ctx, state: bool):
        """Make the author of each action concerning a ticket appear in the server logs.

        Use `True` (Or `yes`) to enable or `False` (or `no`) to disable.
        """
        config = await self.data.guild(ctx.guild).settings.all()

        actual_audit_logs = config["audit_logs"]
        if actual_audit_logs is state:
            await ctx.send(f"Audit Logs is already set on {state}.")
            return

        await self.data.guild(ctx.guild).settings.audit_logs.set(state)
        await ctx.send(f"Audit Logs state registered: {state}.")

    @config.command(name="closeconfirmation", aliases=["confirm"], usage="<true_or_false>")
    async def confirmation(self, ctx, state: bool):
        """Enable or disable Close Confirmation.

        Use `True` (Or `yes`) to enable or `False` (or `no`) to disable.
        """
        config = await self.data.guild(ctx.guild).settings.all()

        actual_close_confirmation = config["close_confirmation"]
        if actual_close_confirmation is state:
            await ctx.send(f"Close Confirmation is already set on {state}.")
            return

        await self.data.guild(ctx.guild).settings.close_confirmation.set(state)
        await ctx.send(f"Close Confirmation state registered: {state}.")

    @config.command(name="message")
    async def message(self, ctx, channel: typing.Optional[discord.TextChannel]=None):
        if channel is None:
            channel = ctx.channel
        button = ActionRow(
            Button(
                style=ButtonStyle.grey,
                label="Open an embassy",
                emoji="????",
                custom_id="create_ticket_button",
                disabled=False
            )
        )
        config = await self.data.guild(ctx.guild).settings.all()
        actual_color = config["color"]
        actual_thumbnail = config["thumbnail"]
        embed: discord.Embed = discord.Embed()
        embed.title = str(config["embed_button"]["title"])
        embed.description = str(config["embed_button"]["description"]).replace('{prefix}', f'{ctx.prefix}')
        embed.set_thumbnail(url=actual_thumbnail)
        embed.color = actual_color
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await channel.send(embed=embed, components=[button])

    async def check_permissions_in_channel(self, permissions: List[str], channel: discord.TextChannel):
        """Function to checks if the permissions are available in a guild.
        This will return a list of the missing permissions.
        """
        return [
            permission
            for permission in permissions
            if not getattr(channel.permissions_for(channel.guild.me), permission)
        ]

    @commands.is_owner()
    @config.command(name="purge", hidden=True)
    async def command_purge(self, ctx, confirmation: typing.Optional[bool]=False):
        """Purge all existing tickets in the config. Does not delete any channels. All commands associated with the tickets will no longer work.
        """
        config = await self.bot.get_cog("TicketTool").get_config(ctx.guild)
        if not confirmation:
            embed: discord.Embed = discord.Embed()
            embed.title = f"Do you really want to purge all the tickets in the config?"
            embed.description = "Does not delete any channels. All commands associated with the tickets will no longer work."
            embed.color = config["color"]
            embed.set_author(name=ctx.author.name, url=ctx.author.avatar_url, icon_url=ctx.author.avatar_url)
            response = await utils(ctx.bot).ConfirmationAsk(ctx, embed=embed)
            if not response:
                return
        count = 0
        to_remove = []
        data = await ctx.bot.get_cog("TicketTool").data.guild(ctx.guild).tickets.all()
        for channel in data:
            count += 1
            to_remove.append(channel)
        for channel in to_remove:
            del data[str(channel)]
        await ctx.bot.get_cog("TicketTool").data.guild(ctx.guild).tickets.set(data)
        await ctx.send(f"{count} tickets have been removed from the config.")
