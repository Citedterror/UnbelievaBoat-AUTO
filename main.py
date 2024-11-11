from asyncio import sleep

from discord import (Client, Message,
                     TextChannel)
from discord.ext import tasks

guild_ids = [
    1272416780618436618
]  # Only servers where the commands will work in (safety feature). Example: [000000000, 000002311, 123689923]. Use https://support.discord.com/hc/articles/206346498 to find ids.

work_wait_time = 31  # Time in minutes between running the work command. Default: 421

collect_wait_time = (
    31  # Time in minutes between running the collect colland. Default: 16
)


@tasks.loop(minutes=work_wait_time)
async def auto_work(work: SlashCommand, channel: TextChannel, dep: SlashCommand):
    await work.__call__(channel=channel)  # Run the work command
    await deposit(dep, channel)  # Deposit your newly earned money


@tasks.loop(minutes=collect_wait_time)
async def auto_collect(collect: SlashCommand, channel: TextChannel, dep: SlashCommand):
    await sleep(2)  # Wait a few seconds for safety
    await collect.__call__(channel=channel)  # Run the collect command
    await deposit(dep, channel)  # Deposit your newly earned money


async def deposit(deposit: SlashCommand, channel: TextChannel):
    await sleep(1)  # Wait a second for safety
    await deposit.__call__(channel=channel, amount="all")  # Run the deposit command


client = Client()  # Define client session


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")  # Let the user know that its running


@client.event
async def on_message(message: Message):
    if (
        message.guild.id in guild_ids
        and message.author.id == client.user.id
        and message.content == "!start"
    ):  # A few safety checks to make sure its not on accident
        await message.delete()  # Delete command message
        application_commands = (
            await message.channel.application_commands()
        )  # Fetches all commands in the channel
        for command in application_commands:
            if command.type == ApplicationCommandType.chat_input:
                if command.id == 901118136529588275:  # Deposit command fetching
                    deposit = command
                if command.id == 901118136529588278:  # Collect command fetching
                    collect = command
                if command.id == 901118136529588281:  # Work command fetching
                    work = command
        if (
            auto_work.is_running() and auto_collect.is_running()
        ):  # Checks if they are already running
            auto_work.restart(
                work, message.channel, deposit
            )  # Restarts work if already running
            auto_collect.restart(
                collect, message.channel, deposit
            )  # Restarts collect if already running
        else:
            auto_work.start(
                work, message.channel, deposit
            )  # Starts work if not running. REMOVE THIS ENTIRE LINE TO DISABLE THE WORK COMMAND
            auto_collect.start(
                collect, message.channel, deposit
            )  # Starts collect if not running. REMOVE THIS ENTIRE LINE TO DISABLE THE COLLECT COMMAND
    if (
        message.guild.id in guild_ids
        and message.author.id == client.user.id
        and message.content == "!stop"
    ):  # A few safety checks to make sure its not on accident
        await message.delete()  # Delete command message
        auto_work.stop()  # Stop working
        auto_collect.stop()  # Stop collecting


client.run("NDA1NTI2NzE2ODI0NDIwMzYy.G-i2C_.QmocrTtdxnCNT322Dv14PycWWnR1CsApxni2eQ")
