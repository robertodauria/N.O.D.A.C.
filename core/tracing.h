#ifndef TRACING_H
#define TRACING_H

#include "core.h"

void dump_format( const format_t *data );

void dump_eqm( float eqm );

void dump_error( float error );

void dump_memory( FILE *fh, const format_t *data, const fdb_t *table );

void dump_results( const float *input,
		   uint in,
		   const neuron_t *neuron,
		   uint out );

#endif // TRACING_H
