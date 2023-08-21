from signalbot import Command, Context
import asyncio

from dalle import generate_image


class DalleCommand(Command):
    def describe(self) -> str:
        return "Respond with Dall-E generated image"

    async def handle(self, c: Context):
        print(c)
        print(dir(c))
        prompt = c.message.text
        await c.start_typing()
        image_b64 = generate_image(prompt)
        await asyncio.sleep(5)
        await c.stop_typing()
        await c.send(
            prompt,
            base64_attachments=[image_b64],
        )
