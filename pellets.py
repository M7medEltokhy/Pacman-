from config import WIDTH, HEIGHT

def make_pellets(grid_w=20, grid_h=15, margin=60):
    pellets = []
    cell_w = (WIDTH - margin * 2) / grid_w
    cell_h = (HEIGHT - margin * 2) / grid_h
    for i in range(grid_w):
        for j in range(grid_h):
            x = int(margin + i * cell_w + cell_w / 2)
            y = int(margin + j * cell_h + cell_h / 2)
            pellets.append([x, y, 6])
    return pellets
