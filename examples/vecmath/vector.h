#pragma once

#include <math.h>

typedef struct {
    float x;
    float y;
} vec2;

vec2    vector_create(float x, float y);
vec2    vector_translate(vec2 a, vec2 b);
float   vector_length(vec2 v);
vec2    vector_normalize(vec2 v);
float   vector_dot(vec2 a, vec2 b); 
