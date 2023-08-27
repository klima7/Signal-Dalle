from abc import ABC, abstractmethod

from signalbot import Command, Context

from translate import from_english


class SafeCommand(Command, ABC):

    async def handle(self, c: Context):
        try:
            await self.handle_save(c)
        except Exception as e:
            await c.send(from_english('⚡⚡ An unexpected error occurred'))
        
    @abstractmethod
    async def handle_save(self, c:Context):
        pass