'''Shared chart style for the notebooks.'''

import os

BAR_COLOR = '#2a78d6'
SURFACE = '#fcfcfb'
INK = '#0b0b0b'
INK_SECONDARY = '#52514e'
MUTED = '#898781'
GRID = '#e1e0d9'
BASELINE = '#c3c2b7'

# one-hue blue ramp, light to dark, for magnitude
BLUE_RAMP = ['#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95', '#0d366b']


def add_title(fig, title, subtitle, height):
    '''Left-aligned title and subtitle at the top of a figure that is `height` inches tall.'''
    fig.text(0.01, 1 - 0.12 / height, title,
             ha='left', va='top', fontsize=13, fontweight='bold', color=INK)
    fig.text(0.01, 1 - 0.38 / height, subtitle,
             ha='left', va='top', fontsize=9, color=INK_SECONDARY)


FIGURE_DIR = 'figures'


def save_figure(fig, name):
    '''Save a figure as figures/<name>.png.'''
    os.makedirs(FIGURE_DIR, exist_ok=True)
    fig.savefig(f'{FIGURE_DIR}/{name}.png', dpi=200, facecolor=fig.get_facecolor())
