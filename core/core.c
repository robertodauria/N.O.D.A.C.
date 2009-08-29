#include <stdio.h>
#include <stdlib.h>
#include "core.h"
#include "parsing.h"
#include "tracing.h"

int main( int argc, char **argv )
{
  iformat idata;
  FILE *ifh;
  ifh = fopen( "../landscape.nod", "rb" );
  if( ifh == NULL )
    return EXIT_FAILURE;
  parse_iformat( ifh, &idata );
  dump_iformat( &idata );
  return EXIT_SUCCESS;
}
