from .imagefunc import *

NODE_NAME = 'Sharp & Soft'

class SharpAndSoft:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):

        enhance_list = ['very sharp', 'sharp', 'soft', 'very soft']

        return {
            "required": {
                "images": ("IMAGE",),
                "enhance": (enhance_list, ),

            },
            "optional": {
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = 'sharp_and_soft'
    CATEGORY = '😺dzNodes/LayerFilter'
    OUTPUT_NODE = True

    def sharp_and_soft(self, images, enhance, ):

        if enhance == 'very sharp':
            filter_radius = 1
            denoise = 0.6
            detail_mult = 2.8
        if enhance == 'sharp':
            filter_radius = 3
            denoise = 0.12
            detail_mult = 1.8
        if enhance == 'soft':
            filter_radius = 8
            denoise = 0.08
            detail_mult = 0.5
        if enhance == 'very soft':
            filter_radius = 15
            denoise = 0.06
            detail_mult = 0.01

        d = int(filter_radius * 2) + 1
        s = 0.02
        n = denoise / 10
        dup = copy.deepcopy(images.cpu().numpy())

        for index, image in enumerate(dup):
            imgB = image
            if denoise > 0.0:
                imgB = cv2.bilateralFilter(image, d, n, d)
            imgG = np.clip(guidedFilter(image, image, d, s), 0.001, 1)
            details = (imgB / imgG - 1) * detail_mult + 1
            dup[index] = np.clip(details * imgG - imgB + image, 0, 1)

        log(f"{NODE_NAME} Processed {dup.shape[0]} image(s).", message_type='finish')
        return (torch.from_numpy(dup),)


NODE_CLASS_MAPPINGS = {
    "LayerFilter: Sharp & Soft": SharpAndSoft
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LayerFilter: Sharp & Soft": "LayerFilter: Sharp & Soft"
}