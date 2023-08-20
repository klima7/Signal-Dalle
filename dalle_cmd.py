from signalbot import Command, Context


class DalleCommand(Command):
    def describe(self) -> str:
        return "Respond with Dall-E generated image"

    async def handle(self, c: Context):
        command = c.message.text
        await c.send(command)
        return
