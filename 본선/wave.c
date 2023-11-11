//
//  main.c
//  wave
//
//  Created by 이민성 on 2023/11/02.
//

#include <stdio.h>

void wave(void)
{
    int i;
    float wave;
    for (i = 1; i <= 31; i++) {
        if (i == 12) {
            wave = 32.1;
            printf("%d day's average wave: %f\n", i, wave);
            printf("Warning !!!!");
            printf("\n");
            printf("\n");
        }
        else if (i == 20) {
            wave = 31.87;
            printf("%d day's average wave: %f\n", i, wave);
            printf("Warning !!!!");
            printf("\n");
            printf("\n");
        }
        else {
            wave = 15.0;
            printf("%d day's average wave: %f\n", i, wave);
            printf("\n");
        }
    }
}

int main(void) {
    wave();
    return 0;
}
