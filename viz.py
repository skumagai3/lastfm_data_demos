'''Shared chart style for the notebooks.'''

import json
import os

import matplotlib as mpl
import numpy as np
from matplotlib import font_manager
from matplotlib.image import BboxImage
from matplotlib.textpath import TextPath
from matplotlib.transforms import Bbox, TransformedBbox
from PIL import Image, ImageDraw

# DejaVu Sans has no CJK glyphs, so artist names like these would show as boxes. Matplotlib tries the
# fonts in this list in order for each character, using whichever of them is installed.
CJK_FONTS = ['Hiragino Sans', 'Apple SD Gothic Neo', 'PingFang SC',
             'Noto Sans CJK JP', 'Noto Sans CJK KR', 'Noto Sans CJK SC', 'Yu Gothic', 'Malgun Gothic', 'Microsoft YaHei']
installed_fonts = {font.name for font in font_manager.fontManager.ttflist}
mpl.rcParams['font.family'] = ['DejaVu Sans'] + [name for name in CJK_FONTS if name in installed_fonts]

# dark theme: the surface and ink colors, plus the blues stepped for a dark background
BAR_COLOR = '#3987e5'
SURFACE = '#1a1a19'
INK = '#f0efec'
INK_SECONDARY = '#c3c2b7'
MUTED = '#898781'
GRID = '#2c2c2a'
BASELINE = '#383835'

# one-hue blue ramp for magnitude, dark to light: the lowest values sit close to the background and the highest stand out
BLUE_RAMP = ['#0d366b', '#184f95', '#256abf', '#3987e5', '#6da7ec', '#9ec5f4', '#cde2fb']

# defaults for anything a chart doesn't color explicitly
mpl.rcParams.update({
    'figure.facecolor': SURFACE,
    'axes.facecolor': SURFACE,
    'savefig.facecolor': SURFACE,
    'text.color': INK,
    'axes.labelcolor': INK_SECONDARY,
    'axes.edgecolor': BASELINE,
    'xtick.color': MUTED,
    'ytick.color': MUTED,
})

PROFILE_JSON = 'profile.json'  # written by 00_ingest.ipynb
PROFILE_IMAGE = 'profile.png'


def circular_avatar(path, size=200):
    '''Crop the image at `path` to a centered square, then mask it to a circle.'''
    image = Image.open(path).convert('RGBA')
    side = min(image.size)
    left, top = (image.width - side) // 2, (image.height - side) // 2
    image = image.crop((left, top, left + side, top + side)).resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size * 4, size * 4), 0)  # drawn at 4x, then shrunk, for a smooth edge
    ImageDraw.Draw(mask).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
    image.putalpha(mask.resize((size, size), Image.LANCZOS))
    return np.asarray(image)


def add_profile(fig):
    '''Profile picture and username in the top-right corner. Does nothing without profile.json.'''
    if not os.path.exists(PROFILE_JSON):
        return
    with open(PROFILE_JSON) as f:
        username = json.load(f)['username']

    width, height = fig.get_size_inches()
    size = 0.42  # picture diameter in inches
    margin_right, margin_top = 0.12, 0.10  # distance from the figure edges, in inches
    if os.path.exists(PROFILE_IMAGE):
        left, bottom = 1 - (margin_right + size) / width, 1 - (margin_top + size) / height
        box = TransformedBbox(Bbox([[left, bottom], [left + size / width, bottom + size / height]]), fig.transFigure)
        picture = BboxImage(box)  # sized in figure coordinates, so it scales with the figure and counts toward a tight bounding box
        picture.set_data(circular_avatar(PROFILE_IMAGE))
        fig.add_artist(picture)
        margin_right += size + 0.08
    # center the glyphs themselves on the picture; va='center' would also count the space below the baseline
    ink = TextPath((0, 0), username, size=9).get_extents()  # in points, relative to the baseline
    baseline = 1 - (margin_top + size / 2) / height - (ink.y0 + ink.y1) / 2 / 72 / height
    fig.text(1 - margin_right / width, baseline, username,
             ha='right', va='baseline', fontsize=9, color=INK_SECONDARY)


def add_title(fig, title, subtitle, height):
    '''Left-aligned title and subtitle at the top of a figure that is `height` inches tall.'''
    fig.text(0.01, 1 - 0.12 / height, title,
             ha='left', va='top', fontsize=13, fontweight='bold', color=INK)
    fig.text(0.01, 1 - 0.38 / height, subtitle,
             ha='left', va='top', fontsize=9, color=INK_SECONDARY)
    add_profile(fig)


FIGURE_DIR = 'figures'


def save_figure(fig, name):
    '''Save a figure as figures/<name>.png.'''
    os.makedirs(FIGURE_DIR, exist_ok=True)
    fig.savefig(f'{FIGURE_DIR}/{name}.png', dpi=200, facecolor=fig.get_facecolor())
