#include <stdio.h>
#include "vector.h"

int main() {
    vec2 a = {1.0f, 0.0f};
    vec2 b = {0.0f, -1.0f};

    printf("Surprisingly enough, the dot product of two perpendicular vectors is %f\n", vector_dot(a, b));

    return 0;
}
