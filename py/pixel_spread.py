import copy
from pymatting import *
from .imagefunc import *

class PixelSpread:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):

        return {
            "required": {
                "image": ("IMAGE", ),  #
                "invert_mask": ("BOOLEAN", {"default": False}),  # 反转mask
                "mask_grow": ("INT", {"default": 0, "min": -999, "max": 999, "step": 1}),
            },
            "optional": {
                "mask": ("MASK",),  #
            }
        }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("image", )
    FUNCTION = 'pixel_spread'
    CATEGORY = '😺dzNodes/LayerMask'
    OUTPUT_NODE = True

    def pixel_spread(self, image, invert_mask, mask_grow, mask=None):

        l_images = []
        l_masks = []
        ret_images = []

        for l in image:
            i = tensor2pil(l)
            l_images.append(i)
            if i.mode == 'RGBA':
                l_masks.append(i.split()[-1])
            else:
                l_masks.append(Image.new('L', i.size, 'white'))
        if mask is not None:
            l_masks = []
            for m in mask:
                if invert_mask:
                    m = 1 - m
                l_masks.append(tensor2pil(m).convert('L'))
        max_batch = max(len(l_images), len(l_masks))

        for i in range(max_batch):

            _image = l_images[i] if i < len(l_images) else l_images[-1]
            _mask = l_masks[i] if i < len(l_masks) else l_masks[-1]
            if mask_grow != 0:
                _mask = expand_mask(image2mask(_mask), mask_grow, 0)  # 扩张，模糊
                _mask = mask2image(_mask)
            i1 = pil2tensor(_image.convert('RGB'))
            _mask = _mask.convert('RGB')
            i_dup = copy.deepcopy(i1.cpu().numpy().astype(np.float64))
            a_dup = copy.deepcopy(pil2tensor(_mask).cpu().numpy().astype(np.float64))
            fg = copy.deepcopy(i1.cpu().numpy().astype(np.float64))

            for index, img in enumerate(i_dup):
                alpha = a_dup[index][:, :, 0]  # convert to single channel
                # trimap = fix_trimap(trimap, 0.01, 0.99)
                # alpha = estimate_alpha_cf(image, trimap, laplacian_kwargs={"epsilon": 1e-6},
                #                           cg_kwargs={"maxiter": 100})
                fg[index], _ = estimate_foreground_ml(img, np.array(alpha), return_background=True)

            ret_images.append(torch.from_numpy(fg.astype(np.float32)))

        log(f'PixelSpread Processed {len(ret_images)} image(s).')
        return (torch.cat(ret_images, dim=0),)

NODE_CLASS_MAPPINGS = {
    "LayerMask: PixelSpread": PixelSpread
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LayerMask: PixelSpread": "LayerMask: PixelSpread"
}