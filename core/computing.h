#ifndef COMPUTING_H
#define COMPUTING_H

#include "core.h"

void see( layer_t *layer, const float *signal );

void think( layer_t *layer, uint dlayers );

void learn( layer_t *layer, uint dlayers, const float *expected );

float collect( layer_t *layer, uint level );

#endif // COMPUTING_H
