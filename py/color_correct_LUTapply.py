from .imagefunc import *

NODE_NAME = 'LUT Apply'

class ColorCorrectLUTapply:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        color_space_list = ['linear', 'log']
        return {
            "required": {
                "image": ("IMAGE", ),  #
                "LUT": (LUT_LIST,),  # LUT文件
                "color_space":  (color_space_list,),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = 'color_correct_LUTapply'
    CATEGORY = '😺dzNodes/LayerColor'
    OUTPUT_NODE = True

    def color_correct_LUTapply(self, image, LUT, color_space):
        ret_images = []
        for i in image:
            i = torch.unsqueeze(i, 0)
            _image = tensor2pil(i)

            lut_file = LUT_DICT[LUT]
            ret_image = apply_lut(_image, lut_file, log=(color_space == 'log'))

            if _image.mode == 'RGBA':
                ret_image = RGB2RGBA(ret_image, _image.split()[-1])
            ret_images.append(pil2tensor(ret_image))

        log(f"{NODE_NAME} Processed {len(ret_images)} image(s).", message_type='finish')
        return (torch.cat(ret_images, dim=0),)

NODE_CLASS_MAPPINGS = {
    "LayerColor: LUT Apply": ColorCorrectLUTapply
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LayerColor: LUT Apply": "LayerColor: LUT Apply"
}