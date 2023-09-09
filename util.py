# Utilitiy functions to generate coordinates
def generate_cls(width, brick_w,  offset=0):
    n = width//(brick_w+1)
    return [offset + i*(brick_w) + (i)*2 for i in range(n)]

def generate_rows(height, brick_h, offset=0):
    n = height//(brick_h+9)
    return (offset + i*(brick_h) + (i)*5 for i in range(n))

# All differnt colours used
colors = [
    (232,99,117),
    (255,161,153),
    (255,208,153),
    (175,214,173),
    (124,182,160)
]
