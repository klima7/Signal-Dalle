import io

import numpy as np
from signalbot import Command, Context, SendAttachment
from PIL import Image
import cv2 as cv

from dalle import edit_image
from translate import to_english


class EditCommand(Command):
    
    IMAGE_MIMES = ['image/png', 'image/jpeg']
    
    def describe(self) -> str:
        return "Respond with Dall-E edited image"

    async def handle(self, c: Context):
        prompt = c.message.text
        attachments = c.message.base64_attachments
        
        # must be image with text to trigger command
        if not (len(attachments) > 0 and prompt):
            return
        
        # single file must be attached
        if not (len(attachments) == 1 and attachments[0].content_type.split('/')[0] == 'image'):
            await c.react('🤔')
            return
        
        await c.react('👍')
        await c.start_typing()
        
        attachment = attachments[0]
        await c.fetch_attachment_data(attachment)
        
        prompt_en = to_english(prompt)
        image = np.array(self._resize_image(Image.open(io.BytesIO(attachment.data)), length=1024)) 
        mask = self._create_mask(image)
        edited = edit_image(image, mask, prompt_en)
        
        await c.stop_typing()
        await c.send(
            prompt_en,
            base64_attachments=[edited]
        )
        
    @staticmethod
    def _resize_image(image, length) -> Image:
        if image.size[0] < image.size[1]:
            resized_image = image.resize((length, int(image.size[1] * (length / image.size[0]))))
            required_loss = (resized_image.size[1] - length)
            resized_image = resized_image.crop(
                box=(0, required_loss / 2, length, resized_image.size[1] - required_loss / 2))
            return resized_image
        else:
            resized_image = image.resize((int(image.size[0] * (length / image.size[1])), length))
            required_loss = resized_image.size[0] - length
            resized_image = resized_image.crop(
                box=(required_loss / 2, 0, resized_image.size[0] - required_loss / 2, length))
            return resized_image
        
    @staticmethod
    def _create_mask(image):
        alpha_channel = np.ones(shape=(image.shape[0], image.shape[1], 1), dtype=image.dtype)*255
        mask = np.concatenate([image, alpha_channel], axis=2)
        binary_mask = cv.inRange(image, (240, 240, 240), (256, 256, 256))
        
        kernel_size = 25
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(kernel_size, kernel_size))
        binary_mask = cv.morphologyEx(binary_mask.astype(np.float32), cv.MORPH_OPEN, kernel).astype(np.bool_)
        binary_mask = cv.morphologyEx(binary_mask.astype(np.float32), cv.MORPH_CLOSE, kernel).astype(np.bool_)
        binary_mask = cv.dilate(binary_mask.astype(np.float32), kernel, iterations = 1).astype(np.bool_)
        
        mask[binary_mask, 3] = 0
        return mask
