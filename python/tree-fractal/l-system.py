import cv2
import numpy as np
import math

SMALL_COEF = 0.4
EXP_COEF = 0

AXIOM = "F++F++F"
NEW = {"F": "F-F++F-F"}
THETA = 180 / 3
DATA_START = np.array([450, 50, 90], dtype="float")
LENGTH = 2
ITERATIONS = 5

AXIOM = "FB"
NEW = {"F": "F-------[F]+[F]+[F]++[F]+[F]+[F]+[F]"}
# ~ NEWF = "-F+F+[+F-F]-[-F+F+F]"
THETA = 360 / 8
DATA_START = np.array([300, 5, 90], dtype="float")
LENGTH = 700
ITERATIONS = 5

STATES = []
DATA = DATA_START.copy()


def easeOutElastic(x):
    c4 = (2 * np.pi) / 3
    if math.isclose(x, 0):
        return 0
    if math.isclose(x, 1):
        return 1
    return pow(2, -10 * x) * np.sin((x * 10 - 0.75) * c4) + 1


def easeOutExpo(x):
    if math.isclose(x, 1):
        return 1
    return 1 - pow(2, -10 * x)


def easeOutBack(x):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(x - 1, 3) + c1 * pow(x - 1, 2);


def calc_dest(data):
    length = LENGTH * SMALL_COEF**(len(STATES)+1)
    a = data[2] * np.pi / 180
    new_data = data.copy()
    new_data[:2] += np.array((np.cos(a), np.sin(a))) * length
    new_data[2] = a
    return new_data


def draw_line(img, data):
    level = ITERATIONS - len(STATES) + 1
    level = 1
    end_data = calc_dest(data)
    cv2.line(img, data[:2].astype("int"), end_data[:2].astype("int"), 0, level, lineType=cv2.LINE_AA)
    return end_data


def exp_angle(x, coef):
    return (np.exp(x/180*coef)-1)/(np.exp(coef)-1)*180

def exp_angle_abs(x, coef):
    return exp_angle(abs(x), coef) * np.sign(x)

def log_angle(x):
    x, s = abs(x), np.sign(x)
    return np.log(x+1)/np.log(180+1)*180 * s
    
def F(img):
    a = DATA[2] % 360
    if a > 180:
        a -= 360
    new_data = DATA.copy()
    new_data[2] = exp_angle_abs(a, EXP_COEF)
    DATA[:2] = draw_line(img, new_data)[:2]
    
def b(img):
    DATA[:2] = calc_dest(DATA)[:2]
    
def ob(img):
    STATES.append(DATA.copy())
    
def cb(img):
    DATA[:] = STATES.pop()

def pa(img):
    DATA[2] += THETA

def ma(img):
    DATA[2] -= THETA
    
def none(img):
    pass

RULES_DICT = {"F": F, "b": b, "[": ob, "]": cb, "+": pa, "-": ma}
    
def draw_it(img):
    for i in AXIOM:
        RULES_DICT.get(i, none)(img)

def main():
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (600,600))
    global AXIOM, ALPHA, POS, EXP_COEF
    for _ in range(ITERATIONS):
        for k, v in NEW.items():
            AXIOM = AXIOM.replace(k, v)
    x = 0
    while(x < 160):
        x += 1
        img = np.zeros((600,600), dtype="uint8")
        img[:] = 255

        DATA[:] = DATA_START
        xx = (x/40)%4
        if xx < 1:
            EXP_COEF = easeOutExpo(xx%1)
        elif xx < 2:
            EXP_COEF = 1-easeOutBack(xx%1)
        elif xx < 3:
            EXP_COEF = -easeOutExpo(xx%1)
        else:
            EXP_COEF = -1+easeOutBack(xx%1)
        if math.isclose(EXP_COEF, 0, abs_tol=0.01):
            EXP_COEF = 0.01
        print(xx, "%f" % EXP_COEF)
        draw_it(img)
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
