#ifndef PARSING_H
#define PARSING_H

#include "core.h"

void parse_iformat( FILE *input, format_t *data, const fdb_t *table );

size_t read_input( const float *input );

#endif // PARSING_H
