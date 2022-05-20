#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import torch
import torch.nn.functional as F
import torchvision.transforms.functional as tvF

import os
import numpy as np
from math import log10
from datetime import datetime
import OpenEXR
from PIL import Image
import Imath

from matplotlib import rcParams
rcParams['font.family'] = 'serif'
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def clear_line():
    """Clears line from any characters."""

    print('\r{}'.format(' ' * 80), end='\r')


def progress_bar(batch_idx, num_batches, report_interval, train_loss):
    """Neat progress bar to track training."""

    dec = int(np.ceil(np.log10(num_batches)))
    bar_size = 21 + dec
    progress = (batch_idx % report_interval) / report_interval
    fill = int(progress * bar_size) + 1
    print('\rBatch {:>{dec}d} [{}{}] Train loss: {:>1.5f}'.format(batch_idx + 1, '=' * fill + '>', ' ' * (bar_size - fill), train_loss, dec=str(dec)), end='')


def time_elapsed_since(start):
    """Computes elapsed time since start."""

    timedelta = datetime.now() - start
    string = str(timedelta)[:-7]
    ms = int(timedelta.total_seconds() * 1000)

    return string, ms


def show_on_epoch_end(epoch_time, valid_time, valid_loss, valid_psnr):
    """Formats validation error stats."""

    clear_line()
    print('Train time: {} | Valid time: {} | Valid loss: {:>1.5f} | Avg PSNR: {:.2f} dB'.format(epoch_time, valid_time, valid_loss, valid_psnr))


def show_on_report(batch_idx, num_batches, loss, elapsed):
    """Formats training stats."""

    clear_line()
    dec = int(np.ceil(np.log10(num_batches)))
    print('Batch {:>{dec}d} / {:d} | Avg loss: {:>1.5f} | Avg train time / batch: {:d} ms'.format(batch_idx + 1, num_batches, loss, int(elapsed), dec=dec))


def plot_per_epoch(ckpt_dir, title, measurements, y_label):
    """Plots stats (train/valid loss, avg PSNR, etc.)."""

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(1, len(measurements) + 1), measurements)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel('Epoch')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    plt.tight_layout()

    fname = '{}.png'.format(title.replace(' ', '-').lower())
    plot_fname = os.path.join(ckpt_dir, fname)
    plt.savefig(plot_fname, dpi=200)
    plt.close()


def load_hdr_as_tensor(img_path):
    """Converts OpenEXR image to torch float tensor."""

    # Read OpenEXR file
    if not OpenEXR.isOpenExrFile(img_path):
        raise ValueError(f'Image {img_path} is not a valid OpenEXR file')
    src = OpenEXR.InputFile(img_path)
    pixel_type = Imath.PixelType(Imath.PixelType.FLOAT)
    dw = src.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    
    # Read into tensor
    tensor = torch.zeros((3, size[1], size[0]))
    for i, c in enumerate('RGB'):
        rgb32f = np.fromstring(src.channel(c, pixel_type), dtype=np.float32)
        tensor[i, :, :] = torch.from_numpy(rgb32f.reshape(size[1], size[0]))
        
    return tensor


def reinhard_tonemap(tensor):
    """Reinhard et al. (2002) tone mapping."""

    tensor[tensor < 0] = 0
    return torch.pow(tensor / (1 + tensor), 1 / 2.2)


def psnr(input, target):
    """Computes peak signal-to-noise ratio."""
    
    return 10 * torch.log10(1 / F.mse_loss(input, target))


def create_montage(img_name, noise_type, save_path, source_t, denoised_t, clean_t, show):
    """Creates montage for easy comparison."""

    fig, ax = plt.subplots(1, 3, figsize=(9, 3))
    fig.canvas.set_window_title(img_name.capitalize()[:-4])

    # Bring tensors to CPU
    source_t = source_t.cpu().narrow(0, 0, 3)
    denoised_t = denoised_t.cpu()
    clean_t = clean_t.cpu()
    
    source = tvF.to_pil_image(source_t)
    denoised = tvF.to_pil_image(torch.clamp(denoised_t, 0, 1))
    clean = tvF.to_pil_image(clean_t)

    # Build image montage
    psnr_vals = [psnr(source_t, clean_t), psnr(denoised_t, clean_t)]
    titles = ['Input: {:.2f} dB'.format(psnr_vals[0]),
              'Denoised: {:.2f} dB'.format(psnr_vals[1]),
              'Ground truth']
    zipped = zip(titles, [source, denoised, clean])
    for j, (title, img) in enumerate(zipped):
        ax[j].imshow(img)
        ax[j].set_title(title)
        ax[j].axis('off')

    # Open pop up window, if requested
    if show > 0:
        plt.show()

    # Save to files
    fname = os.path.splitext(img_name)[0]
    source.save(os.path.join(save_path, f'{fname}-{noise_type}-noisy.png'))
    denoised.save(os.path.join(save_path, f'{fname}-{noise_type}-denoised.png'))
    fig.savefig(os.path.join(save_path, f'{fname}-{noise_type}-montage.png'), bbox_inches='tight')


class AvgMeter(object):
    """Computes and stores the average and current value.
    Useful for tracking averages such as elapsed times, minibatch losses, etc.
    """

    def __init__(self):
        self.reset()


    def reset(self):
        self.val = 0
        self.avg = 0.
        self.sum = 0
        self.count = 0


    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
