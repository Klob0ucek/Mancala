# Mancala is a group of board games for two players. In each of these
# games you move stones from one dent to another.
#
# In this program, I tried to implement a game inspired by game of Kalaha.
# For more informaation read those links:
#
# ‹https://en.wikipedia.org/wiki/Mancala›
# ‹https://en.wikipedia.org/wiki/Kalah›
#
# Board for a game of Kalaha can look something like this, where each letter
# represents a dent on the game board.
#
#  ╭───────╮╭───╮╭───╮╭───╮╭───╮╭───╮╭───╮╭───────╮
#  │       ││ M ││ L ││ K ││ J ││ I ││ H ││       │
#  │   N   │╰───╯╰───╯╰───╯╰───╯╰───╯╰───╯│       │
#  │       │╭───╮╭───╮╭───╮╭───╮╭───╮╭───╮│   G   │
#  │       ││ A ││ B ││ C ││ D ││ E ││ F ││       │
#  ╰───────╯╰───╯╰───╯╰───╯╰───╯╰───╯╰───╯╰───────╯
#
# In this game there are two player that takes turns in moving their stones.
# Each player has six "small dents" that are on his side of the board ([A, B,
# C, D, E, F] and [H, I, J, K, L, M]) and a goal - a "big dent" to the right
# each players small dent. In the beggining, all small dents have same number
# of stones (usually 3). Each turn look something like this:
#
# • Player picks a small dent with some stones in it and takes all the stones.
# • Then he puts the stones to the following dents counter-clockwise including
#   his own goal and opponenets small dents until there are no stones eft in
#   his hand.
#   - for example: if player picks C, then he will put stones into dents D, E,
#   F, G, H, I, J, K, L, M, A, B, C until he runs out of stones.
# • If player puts a stone to one of this small dents that is empty, he takes
#   all stones from corresponding opponents small dent and puts it to his bank. 
#   - for exmaple: if player puts a lst stone to dent D, and opponent has some
#   stones in J, then the player takes all the stones from J and D and puts it
#   into his goal.
# • If a player puts the last stone into their own goal, you can play again.
#
# The game ends when a player has no more legal moves (there are no stones
# in his small dents). Then if the opponent has some stones in his dents,
# he puts them into his goal. The player with more stones int their goal wins.

def init(size, start):
    p1 = []
    for _ in range(size):
        p1.append(start)
    p1.append(0)
    p2 = p1.copy()
    return p1, p2


INVALID_POSITION = 0
EMPTY_POSITION = 1
ROUND_OVER = 2
PLAY_AGAIN = 3


def play(our, their, position):
    if position < 0 or position >= (len(our) - 1):
        return INVALID_POSITION

    if our[position] == 0:
        return EMPTY_POSITION

    hand = our[position]
    our[position] = 0
    side = 0

    while hand > 0:
        current = our if (side % 2 == 0) else their

        for i in range(position + 1, len(current) + 1):
            if i == len(current):
                break

            if side % 2 == 1 and i == len(current) - 1:
                break

            if hand == 1:
                if i == len(current) - 1:
                    current[i] += 1
                    hand -= 1
                    return PLAY_AGAIN
                if current[i] == 0 and their[-i - 2] > 0 and side % 2 == 0:
                    hand += their[-i - 2]
                    their[-i - 2] = 0
                    current[-1] += hand
                else:
                    current[i] += 1
                    hand -= 1
                return ROUND_OVER
            current[i] += 1
            hand -= 1

        side += 1
        position = -1


def main():
    # --- init ---

    assert init(6, 3) \
        == ([3, 3, 3, 3, 3, 3, 0], [3, 3, 3, 3, 3, 3, 0])

    assert init(9, 7) \
        == ([7, 7, 7, 7, 7, 7, 7, 7, 7, 0], [7, 7, 7, 7, 7, 7, 7, 7, 7, 0])

    # --- play ---

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, -1) == INVALID_POSITION
    assert our == [3, 0, 6, 0]
    assert their == [3, 3, 3, 0]

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, 0) == PLAY_AGAIN
    assert our == [0, 1, 7, 1]
    assert their == [3, 3, 3, 0]

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, 1) == EMPTY_POSITION
    assert our == [3, 0, 6, 0]
    assert their == [3, 3, 3, 0]

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, 2) == ROUND_OVER
    assert our == [4, 0, 0, 6]
    assert their == [4, 0, 4, 0]

    our = [3, 0, 6, 0]
    their = [3, 3, 3, 0]
    assert play(our, their, 3) == INVALID_POSITION
    assert our == [3, 0, 6, 0]
    assert their == [3, 3, 3, 0]

    our = [0, 4, 0]
    their = [0, 0, 0]
    play(our, their, 1)


if __name__ == '__main__':
    main()
