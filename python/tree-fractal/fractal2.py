import cv2
import numpy as np
import math

ANGLE = 45
START_ANGLE = ANGLE * 3
SMALL_COEF = 0.4
EXP_COEF = 0.1

def draw_line(img, start, angle, length, level):
    angle = angle * np.pi / 180
    end = (start + np.array((np.cos(angle), np.sin(angle))) * length).astype("int")
    cv2.line(img, start, end, 0, level, lineType=cv2.LINE_AA)
    return end
    
def exp_angle(x, coef):
    return (np.exp(x/180*coef)-1)/(np.exp(coef)-1)*180
    
def log_angle(x):
    x, s = abs(x), np.sign(x)
    return np.log(x+1)/np.log(180+1)*180 * s
    
def do_iter(img, start, angle, length, iteration, coef, small_coef = 1):
    if iteration == 0:
        return
    for i in range(7):
        angl = angle - START_ANGLE + i * ANGLE
        angl2 = exp_angle(angl, coef)
        angl2 = angl
        end = draw_line(img, start, angl2, length * small_coef, iteration)
        do_iter(img, end, angl, length * 0.8, iteration - 1, coef, small_coef * SMALL_COEF)

def main():
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    # ~ out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (1024,600))
    x = 0
    while(1):
        x += 1
        img = np.zeros((600,600), dtype="uint8")
        img[:] = 255

        end = draw_line(img, (300, 100), 90, 200, 6)
        val = (np.sin(x/20)+1)/2
        do_iter(img, end, 90, 150, 5, val)
        img = img[::-1,:]

        cv2.imshow("img", img)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        # ~ out.write(img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    # ~ out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
