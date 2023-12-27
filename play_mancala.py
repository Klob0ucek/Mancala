import tkinter as tk

import mancala_logic as student

# game parameters; feel free to change them
SIZE = 6
START = 3

BORDER = 32
CELL_SIZE = 64
MSG_FONT = ('system', '12')
FONT = ('system', '16')
BANK_FONT = ('system', '32')

TOP = 2 * BORDER
BOTTOM = 2 * BORDER + 2 * CELL_SIZE
LEFT = BORDER
RIGHT = BORDER + (SIZE + 4) * CELL_SIZE
LBOUND = LEFT + 2 * CELL_SIZE
RBOUND = RIGHT - 2 * CELL_SIZE


class Game:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.top, self.bottom = student.init(SIZE, START)
        self.over = False
        self.player = 0


def draw_cell(canvas: tk.Canvas, x: int, y: int,
              num: int, fill: str = "") -> None:
    canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=fill)
    canvas.create_text(x + CELL_SIZE // 2, y + CELL_SIZE // 2,
                       text=str(num), font=FONT)


def draw(canvas: tk.Canvas, game: Game, msg: str = "") -> None:
    canvas.delete('all')

    canvas.create_rectangle(LEFT, TOP, RIGHT, BOTTOM)

    for i in range(SIZE):
        x = LEFT + (2 + i) * CELL_SIZE
        for y, row, index in ((TOP, game.top, SIZE - 1 - i),
                              (TOP + CELL_SIZE, game.bottom, i)):
            draw_cell(canvas, x, y, row[index])

    for x, row in ((LEFT + CELL_SIZE, game.top),
                   (RIGHT - CELL_SIZE, game.bottom)):
        canvas.create_text(x, TOP + CELL_SIZE,
                           text=str(row[-1]), font=BANK_FONT)

    canvas.create_text((LEFT + RIGHT) // 2, BOTTOM + 2 * BORDER,
                       text=msg, font=MSG_FONT)

    if game.over:
        return

    if game.player == 0:
        y = BOTTOM + BORDER
        which = "Bottom"
    else:
        y = BORDER
        which = "Top"

    canvas.create_text((LEFT + RIGHT) // 2, y,
                       text=which + " player's turn", font=MSG_FONT)


def reset_and_draw(canvas: tk.Canvas, game: Game) -> None:
    game.reset()
    draw(canvas, game)


def click(event: tk.Event, canvas: tk.Canvas, game: Game) -> None:
    # ignore clicks
    if (game.over
            # not on active player's side
            or (event.y < TOP + CELL_SIZE) == (game.player == 0)
            # outside
            or not (TOP < event.y < BOTTOM and LBOUND < event.x < RBOUND)
            # directly on boundary lines
            or (event.x - LBOUND) % CELL_SIZE == 0
            or event.y == TOP + CELL_SIZE):
        return

    i = (event.x - LBOUND) // CELL_SIZE
    our, their = game.bottom, game.top

    if game.player == 1:
        i = SIZE - 1 - i
        our, their = their, our

    result = student.play(our, their, i)

    assert result != student.INVALID_POSITION, \
        "This result should not be possible here!"

    if result == student.EMPTY_POSITION:
        msg = "This position is empty. Try again."
    elif result == student.PLAY_AGAIN:
        msg = "Last token ended in the bank. Play again."
    else:
        msg = "Round over. Switching to the other player."
        game.player = 1 - game.player
        our, their = their, our

    if sum(our) == our[-1]:
        game.over = True
        their[-1] = sum(their)
        for i in range(len(their) - 1):
            their[i] = 0

        msg = "Game over. "
        if game.top[-1] > game.bottom[-1]:
            msg += "Top player won!"
        elif game.top[-1] < game.bottom[-1]:
            msg += "Bottom player won!"
        else:
            msg += "It's a draw!"

    draw(canvas, game, msg)


def main() -> None:
    root = tk.Tk()
    canvas = tk.Canvas(
        width=RIGHT + BORDER,
        height=BOTTOM + 3 * BORDER,
    )

    game = Game()
    draw(canvas, game)

    canvas.bind("<Button-1>", lambda ev: click(ev, canvas, game))
    canvas.bind_all("r", lambda _: reset_and_draw(canvas, game))
    canvas.bind_all("q", lambda _: root.destroy())

    canvas.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
