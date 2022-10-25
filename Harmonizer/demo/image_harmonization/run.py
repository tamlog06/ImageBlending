import os
import argparse
import numpy as np
from tqdm import tqdm
from PIL import Image

import torch
import torchvision.transforms.functional as tf

from src import model


if __name__ == '__main__':
    # define/parse cmd arguments
    parser = argparse.ArgumentParser()
    # parser.add_argument('--input-path', type=str, required=True, help='')
    parser.add_argument('--input-path', type=str, required=True, help='image path')
    parser.add_argument('--output-path', type=str, required=True, help='output path')
    parser.add_argument('--pretrained', type=str, default='./pretrained/harmonizer.pth', help='')
    args = parser.parse_known_args()[0]

    print('\n')
    print('================================================================================')
    print('Image Harmonization')
    print('--------------------------------------------------------------------------------')
    print('  - Input Path: {0}'.format(args.input_path))
    print('  - Output Path: {0}'.format(args.output_path))
    print('  - Pretrained Model: {0}'.format(args.pretrained))
    print('================================================================================')
    print('\n')
    
    # check cmd argments
    if not os.path.exists(args.input_path):
        print('Cannot find the input path: {0}'.format(args.input_path))
        exit()
    if not os.path.exists(os.path.join(args.input_path, 'shadowfree')):
        print('Cannot find the shadowfree images in the input path: {0}'.format(os.path.join(args.input_path, 'shadowfree')))
        exit()
    if not os.path.exists(os.path.join(args.input_path, 'foreground_object_mask')):
        print('Cannot find the foreground_object masks in the input path: {0}'.format(os.path.join(args.input_path, 'foreground_object_mask')))
        exit()
    if not os.path.exists(args.pretrained):
        print('Cannot find the pretrained model: {0}'.format(args.pretrained))
        exit()

    # create output path
    os.makedirs(args.output_path, exist_ok=True)
    print('The harmonized images will be saved in: {0}\n'.format(args.output_path))

    # pre-defined arguments
    cuda = torch.cuda.is_available()
    
    # create/load the harmonizer model
    print('Create/load Harmonizer...')
    harmonizer = model.Harmonizer()
    if cuda:
        harmonizer = harmonizer.cuda()
    harmonizer.load_state_dict(torch.load(args.pretrained), strict=True)
    harmonizer.eval()

    print('Process...')
    # inputs = os.listdir(os.path.join(args.input_path, 'composite'))
    inputs = os.listdir(os.path.join(args.input_path, 'shadowfree'))
    pbar = tqdm(inputs, total=len(inputs), unit='image')
    for i, input_path in enumerate(pbar):
        # load the input
        comp = Image.open(os.path.join(args.input_path, 'shadowfree', input_path)).convert('RGB')
        mask = Image.open(os.path.join(args.input_path, 'foreground_object_mask', input_path)).convert('1')
        if comp.size[0] != mask.size[0] or comp.size[1] != mask.size[1]:
            print('The size of the composite image and the mask are inconsistent')
            exit()

        comp = tf.to_tensor(comp)[None, ...]
        mask = tf.to_tensor(mask)[None, ...]

        if cuda:
            comp = comp.cuda()
            mask = mask.cuda()

        # harmonization
        with torch.no_grad():
            arguments = harmonizer.predict_arguments(comp, mask)
            harmonized = harmonizer.restore_image(comp, mask, arguments)

        # save the result
        harmonized = np.transpose(harmonized[0].cpu().numpy(), (1, 2, 0)) * 255
        harmonized = Image.fromarray(harmonized.astype(np.uint8))
        harmonized.save(os.path.join(args.output_path, input_path))

    print('Finished.')
    print('\n')

