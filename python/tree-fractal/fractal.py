import cv2
import numpy as np
import math

ANGLE = 20
START_ANGLE = ANGLE * 1.5
EXP_COEF = 0.1

def draw_line(img, start, angle, length):
    angle = angle * np.pi / 180
    end = (start + np.array((np.cos(angle), np.sin(angle))) * length).astype("int")
    cv2.line(img, start, end, 255)
    return end
    
def exp_angle(x, coef):
    return (np.exp(x/180*coef)-1)/(np.exp(coef)-1)*180
    
def log_angle(x):
    x, s = abs(x), np.sign(x)
    return np.log(x+1)/np.log(180+1)*180 * s
    
def do_iter(img, start, angle, length, iteration, coef):
    if iteration == 0:
        return
    for i in range(4):
        angl = angle - START_ANGLE + i * ANGLE
        angl2 = exp_angle(angl, coef)
        end = draw_line(img, start, angl2, length)
        do_iter(img, end, angl, length * 0.8, iteration - 1, coef)

def main():
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (1024,600))
    x = 0
    while(1):
        x += 1
        img = np.zeros((600,1024), dtype="uint8")

        end = draw_line(img, (512, 100), 90, 100)
        do_iter(img, end, 90, 100, 5, (np.sin(x/20)+1)/2)
        img = img[::-1,:]

        cv2.imshow("img", img)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        out.write(img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
