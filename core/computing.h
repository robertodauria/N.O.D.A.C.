#ifndef COMPUTING_H
#define COMPUTING_H

#include "core.h"
#include "fdb.h"

void see( layer_t *layer, const float *signal, const fdb_t *table );

void think( layer_t *layer, uint layers, const fdb_t *table );

void learn( layer_t *layer,
	    uint layers,
	    const float *expected,
	    const fdb_t *table );

#endif // COMPUTING_H
