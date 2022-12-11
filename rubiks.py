
HEX_COLORS = {
        'W': '#000000',
        'B': '#0000ff',
        'G': '#00ff00',
        'O': '#ffa500',
        'R': '#ff0000',
        'Y': '#ffff00',
        }

class Rubiks:
    COLORS = 'WYROBG'

    def __init__(self):
        self.sides = [color for color in self.COLORS for _ in range(9)]

def draw(painter, cube):
    pass
