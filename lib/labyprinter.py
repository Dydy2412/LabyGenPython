##--Dydy2412---##
from PIL import Image, ImageDraw

def print_to_png(vwalls, hwalls, L, l, walls_size, line_width, name_file):
    img = Image.new('RGB', (walls_size*(l+2)+line_width, walls_size*(L+2)+line_width), color = 'white')
    imgd = ImageDraw.Draw(img)

    for i in range(len(vwalls)):
        for j in range(len(vwalls[i])):
            x1 = walls_size*(j+1)
            y1 = walls_size*(i+1)
            y2 = y1+walls_size+int(line_width/2)
            if not vwalls[i][j]:
                imgd.line([(x1,y1), (x1,y2)], fill='black', width=line_width, joint=None)

    for i in range(len(hwalls)):
        for j in range(len(hwalls[i])):
            x1 = walls_size*(j+1)
            y1 = walls_size*(i+1)
            x2 = x1+walls_size+int(line_width/2)
            if not hwalls[i][j]:
                imgd.line([(x1,y1), (x2,y1)], fill='black', width=line_width, joint=None)

    img.save(name_file)