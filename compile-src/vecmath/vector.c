#include <math.h>
#include "vector.h"

vec2 vector_create(float x, float y) {
    vec2 r;
        r.x = x;
        r.y = y;

    return r;
}

vec2 vector_translate(vec2 a, vec2 b) {
    return vector_create(a.x + b.x, a.y + b.y);
}

float vector_length(vec2 v) {
    return sqrt(v.x*v.x + v.y*v.y);
}

vec2 vector_normalize(vec2 v) {
    float l = vector_length(v);
    return vector_create(v.x/l, v.y/l);
}

float vector_dot(vec2 a, vec2 b) {
    return a.x*b.x + a.y*b.y;
}
