from .imagefunc import *

class ColorCorrectYUV:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):

        return {
            "required": {
                "image": ("IMAGE", ),  #
                "Y": ("INT", {"default": 0, "min": -255, "max": 255, "step": 1}),
                "U": ("INT", {"default": 0, "min": -255, "max": 255, "step": 1}),
                "V": ("INT", {"default": 0, "min": -255, "max": 255, "step": 1}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = 'color_correct_YUV'
    CATEGORY = '😺dzNodes/LayerColor'
    OUTPUT_NODE = True

    def color_correct_YUV(self, image, Y, U, V):

        _y, _u, _v = tensor2pil(image).convert('YCbCr').split()
        if Y != 0 :
            _y = image_gray_offset(_y, Y)
        if U != 0 :
            _u = image_gray_offset(_u, U)
        if V != 0 :
            _v = image_gray_offset(_v, V)
        ret_image = image_channel_merge((_y, _u, _v), 'YCbCr')

        return (pil2tensor(ret_image),)

NODE_CLASS_MAPPINGS = {
    "LayerColor: YUV": ColorCorrectYUV
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LayerColor: YUV": "LayerColor: YUV"
}