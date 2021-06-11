#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>

const int minIters = 128;
const int maxIters = 256;
const int sz[2] = {512, 512};
const float minV[2] = {-3, -1};
const float maxV[2] = {1, 1};
//const float minV[2] = {-0.0, -1.0};
//const float maxV[2] = {1, 1};
const float inf = 20;

float prop(int x, int i) {
    return (maxV[i]-minV[i])*((float)x)/((float)sz[i])+minV[i];
}

int main()
{
    //float (*pts)[3] = (void*)calloc((size_t)(maxIters-minIters)*sz[0]*sz[1] * 3, sizeof(float));
    float pt[3];
    int pts_i = 0, j, k;
    float cords[2], cur_abs, last_abs;
    float complex z, c;
    FILE * f = fopen("out.bin", "wb");

    for (int i = 0; i < sz[0]; i++) {
        for (j = 0; j < sz[1]; j++) {
            cords[0] = prop(i, 0);
            cords[1] = prop(j, 1);
            z = 0;
            c = cords[0]+cords[1]*I;
            last_abs = -100.f;
            for (k = 0; k < maxIters; k++) {
                //z = z + z*z*c - 4;
                z = z*z + c;
                cur_abs = cabs(z);
                if (cur_abs > inf || fabs(last_abs - cur_abs) < 0.0000000001) {
                    break;
                }
                last_abs = cur_abs;
                if (k > minIters) {
                    pt[0] = cimag(c);
                    pt[1] = creal(c);
                    //pt[2] = -cur_abs / 100;
                    pt[2] = cur_abs;
                    pts_i++;
                    fwrite(pt, 3, sizeof(float), f);
                }
            }
        }
    }
    printf("Points: %i\n", pts_i);
    fclose(f);
    //free(pts);
    return 0;
}
