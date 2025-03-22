from p5 import *

board = []
generation = 0
w = 10
width = 400
height = 200
columns = 0
rows = 0
blocks = []
block_col = 0
block_row = 0
f = None
animating = False
margolus_switch = 0

load_msg = True
load_header = False
load_footer = False
final_gen = 0

def create2DArray(columns, rows):
    arr = [[]] * columns
    for i in range(columns):
        arr[i] = [0] * rows
    return arr


def load_message():
    """
    Loads in the original Sign in Space binary message.
    In particular, decomposes the message into the "header," "footer," and "contents."
    Returns each of these as separate int lists.
    """
    with open("data17.txt", "r") as f:
        transmission = f.read()
    transmission = str(transmission)
    header = transmission[:80]
    footer = transmission[65616:]
    message = transmission[80:65616]

    components = [message, header, footer]
    for msg in components:
        components[components.index(msg)] = list(msg)

    for msg in components:
        for i in range(len(msg)):
            msg[i] = int(msg[i])

    for msg in components:
        print(msg)
        print(type(msg))
        print(type(msg[0]))

    return components[0], components[1], components[2]


# Custom code for reshaping a list into a 2D array
def reshape(list, cols, rows):
    new_list = create2DArray(cols, rows)
    print(len(list))
    print(cols)
    print(rows)

    assert len(list) == cols * rows

    index = 0
    while index < len(list):
        for i in range(cols):
            for j in range(rows):
                new_list[i][j] = list[index]
                index += 1
    return new_list


# Input 2x2 matrix, get matrix rotated counter-clockwise once
def ccw(matrix):
    new_mat = matrix.copy()
    up_left = matrix[1][0]
    bot_left = matrix[0][0]
    up_right = matrix[1][1]
    bot_right = matrix[0][1]

    new_mat[0][0] = up_left
    new_mat[0][1] = bot_left
    new_mat[1][0] = up_right
    new_mat[1][1] = bot_right
    return new_mat


# Start from scratch
def setup():
    global width, height, board, w, generation, columns, rows, f, load_msg
    global load_header, load_footer, animating, blocks, block_col, block_row
    global margolus_switch, final_gen

    f = create_font("arial.ttf", 12, )
    generation = 0
    margolus_switch = 0
    animating = True
    load_msg = True
    load_header = False
    load_footer = False
    final_gen = 6625

    if load_msg:
        w = 3
        width = 256 * w
        height = 256 * w
    elif load_header or load_footer:
        w = 30
        width = 40 * w
        height = 2 * w

    columns = int(width / w)
    rows = int(height / w)

    size(width, height + 16) # Extra height for generation counter
    background(255)
    no_stroke()

    message, header, footer = load_message()

    if load_msg:
        board = reshape(message, columns, rows)
    elif load_header:
        board = reshape(header, columns, rows)
        no_loop()
    elif load_footer:
        board = reshape(footer, columns, rows)
        no_loop()

def draw():
    global board, generation, columns, rows, w, f, height, width, animating, blocks
    global block_col, block_row, margolus_switch, final_gen

    if generation > -1:
        fill(0)
        rect((0,0),width,height)

        # Generation counter at bottom of screen
        fill(255)
        rect((0, height), width, 16)

        text_font(f)
        fill(0)
        text("Generation: " + str(generation), (0, height))

        # Draw desired board
        for i in range(columns):
            for j in range(rows):
                if board[i][j] == 1:
                    fill(255)
                    square(i * w, j * w, w)
        save_frame("images/sign_" + str(generation) + ".png")

    if animating and load_msg:
        # Basic outline for the function:
        # Rotate CCW twice. (constitutes 1 generation)
        # Then switch grid perspective (this is the Margolus switch)
        # Then rotate CCW twice (constitutes 2nd generation)
        # Then repeat

        nextgen = create2DArray(columns, rows)

        # Run over first block set
        for i in range(margolus_switch, columns, 2):
            for j in range(margolus_switch, rows, 2):
                # print ("generation: " + str(generation))
                # print("(" + str(i) + "," + str(j) + ")")

                # We treat the board as a torus.
                # Get 2x2 block neighborhood
                if i == columns - 1:
                    if j == rows - 1:
                        nbd = [[board[i][j], board[i][0]], [board[0][j], board[0][0]]]
                    else:
                        nbd = [[board[i][j], board[i][j+1]],[board[0][j], board[0][j+1]]]
                elif j == rows - 1:
                    nbd = [[board[i][j], board[i][0]], [board[i + 1][j], board[i + 1][0]]]
                else:
                    nbd = [[board[i][j], board[i][j + 1]], [board[i + 1][j], board[i + 1][j + 1]]]

                # Compute number of live cells
                nbd_sum = 0
                for x in range(2):
                    for y in range(2):
                        nbd_sum += nbd[x][y]

                # If 1 live cell, rotate CCW twice. Otherwise, do nothing.
                if nbd_sum == 1:
                    next_nbd = nbd.copy()
                    nbd = ccw(next_nbd) # Rotate ccw twice (can mess with this)

                # Next, we need to update nextgen (maintaining the toroidal shape)
                if i == columns - 1:
                    if j == rows - 1:
                        nextgen[i][j] = nbd[0][0]
                        nextgen[0][j] = nbd[0][1]
                        nextgen[i][0] = nbd[1][0]
                        nextgen[0][0] = nbd[1][1]
                    else:
                        nextgen[i][j] = nbd[0][0]
                        nextgen[i][j+1] = nbd[0][1]
                        nextgen[0][j] = nbd[1][0]
                        nextgen[0][j+1] = nbd[1][1]
                elif j == rows - 1:
                    nextgen[i][j] = nbd[0][0]
                    nextgen[i][0] = nbd[0][1]
                    nextgen[i+1][j] = nbd[1][0]
                    nextgen[i+1][0] = nbd[1][1]
                else:
                    for x in range(2):
                        for y in range(2):
                            nextgen[i + x][j + y] = nbd[x][y]

                # Checking the Margolus grid
                # fill(margolus_switch * 255, 0, (1 - margolus_switch) * 255)
                # stroke(0)
                # square(i * w, j * w, w*2)

        # Hit the Margolus switch (changes grid blocks)
        if margolus_switch == 0:
            margolus_switch = 1
        elif margolus_switch == 1:
            margolus_switch = 0

        generation += 1
        board = nextgen.copy()
        del nextgen

        if generation == final_gen + 1:
            no_loop()


if __name__ == '__main__':
    run()

