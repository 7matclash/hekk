import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint


def main(stdscr):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    snk_x = sw // 4
    snk_y = sh // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2],
    ]
    food = [sh // 2, sw // 2]
    w.addch(food[0], food[1], curses.ACS_PI)

    key = KEY_RIGHT
    score = 0

    while True:
        next_key = w.getch()
        if next_key != -1:
            key = next_key

        if key == KEY_RIGHT:
            new_head = [snake[0][0], snake[0][1] + 1]
        elif key == KEY_LEFT:
            new_head = [snake[0][0], snake[0][1] - 1]
        elif key == KEY_UP:
            new_head = [snake[0][0] - 1, snake[0][1]]
        elif key == KEY_DOWN:
            new_head = [snake[0][0] + 1, snake[0][1]]
        else:
            continue

        snake.insert(0, new_head)

        if (
            snake[0][0] in [0, sh] or
            snake[0][1] in [0, sw] or
            snake[0] in snake[1:]
        ):
            msg = "Game Over!"
            w.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            w.refresh()
            curses.napms(2000)
            break

        if snake[0] == food:
            score += 1
            food = None
            while food is None:
                nf = [randint(1, sh - 2), randint(1, sw - 2)]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        w.addch(snake[0][0], snake[0][1], '#')

    w.addstr(sh - 1, 0, f"Score: {score}  Press any key to exit.")
    w.timeout(-1)
    w.getch()


if __name__ == "__main__":
    curses.wrapper(main)
