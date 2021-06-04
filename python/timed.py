
import time

FPS = 16
TICK = 1 / FPS


def main():
    while True:
        cur_time = time.time()
        next_time = cur_time - cur_time % TICK + TICK
        print(cur_time, next_time)
        time.sleep(0.005)
        sleep = next_time - time.time()
        if sleep > 0:
            time.sleep(sleep)


main()
