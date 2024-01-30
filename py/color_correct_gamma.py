from .imagefunc import *

class ColorCorrectGamma:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):

        return {
            "required": {
                "image": ("IMAGE", ),
                "gamma": ("FLOAT", {"default": 1, "min": 0.1, "max": 10, "step": 0.01}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = 'color_correct_gamma'
    CATEGORY = '😺dzNodes/LayerColor'
    OUTPUT_NODE = True

    def color_correct_gamma(self, image, gamma):

        ret_image = gamma_trans(tensor2pil(image), gamma)

        return (pil2tensor(ret_image),)

NODE_CLASS_MAPPINGS = {
    "LayerColor: Gamma": ColorCorrectGamma
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LayerColor: Gamma": "LayerColor: Gamma"
}