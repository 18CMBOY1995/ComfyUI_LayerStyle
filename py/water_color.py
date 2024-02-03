from .imagefunc import *

class WaterColor:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):

        return {
            "required": {
                "image": ("IMAGE", ),
                "line_density": ("INT", {"default": 50, "min": 1, "max": 100, "step": 1}),  # 透明度
                "opacity": ("INT", {"default": 100, "min": 0, "max": 100, "step": 1}),  # 透明度
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = 'water_color'
    CATEGORY = '😺dzNodes/LayerFilter'
    OUTPUT_NODE = True

    def water_color(self, image, line_density, opacity
                  ):

        _canvas = tensor2pil(image).convert('RGB')
        _image = image_watercolor(_canvas, level=101-line_density)
        ret_image = chop_image(_canvas, _image, 'normal', opacity)

        return (pil2tensor(ret_image),)

NODE_CLASS_MAPPINGS = {
    "LayerFilter: WaterColor": WaterColor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LayerFilter: WaterColor": "LayerFilter: WaterColor"
}