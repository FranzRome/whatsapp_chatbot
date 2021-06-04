import asyncio
from cleverbotfree import CleverbotAsync
from cleverbotfree import Cleverbot


@Cleverbot.connect
def chat(bot, user_prompt, bot_prompt):
    """Example code using cleverbotfree sync api with decorator."""
    while True:
        user_input = input(user_prompt)
        if user_input == "quit":
            break
        reply = bot.single_exchange(user_input)
        print(bot_prompt, reply)
    bot.close()


chat("User: ", "Cleverbot:")


@CleverbotAsync.connect
async def async_chat(bot, user_prompt, bot_prompt):
    """Example code using cleverbotfree async api with decorator."""
    while True:
        user_input = input(user_prompt)
        if user_input == "quit":
            break
        reply = await bot.single_exchange(user_input)
        print(bot_prompt, reply)
    await bot.close()

#asyncio.run(async_chat("User: ", "Cleverbot:"))
