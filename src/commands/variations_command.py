import io
import os

import numpy as np
from signalbot import Command, Context
from PIL import Image
import cv2 as cv

from dalle import create_variations
from utils import resize_image


class VariationsCommand(Command):
    
    VARIATIONS_COUNT = int(os.environ.get("VARIATIONS_COUNT", 1))
    
    def describe(self) -> str:
        return "Respond with image variations created with DALL-E"

    async def handle(self, c: Context):
        prompt = c.message.text
        attachments = c.message.base64_attachments
        
        # must be image without text to trigger command
        if not (len(attachments) > 0 and not prompt):
            return
        
        # single file must be attached
        if not (len(attachments) == 1 and attachments[0].content_type.split('/')[0] == 'image'):
            await c.react('🤔')
            return
        
        await c.react('👍')
        await c.start_typing()
        
        attachment = attachments[0]
        await c.fetch_attachment_data(attachment)
        
        image = np.array(resize_image(Image.open(io.BytesIO(attachment.data)), length=1024)) 
        variations = create_variations(image, self.VARIATIONS_COUNT)
        
        await c.stop_typing()
        await c.send(
            '',
            base64_attachments=variations
        )
