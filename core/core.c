#include <stdio.h>
#include <stdlib.h>
#include "core.h"
#include "parsing.h"
#include "tracing.h"
#include "computing.h"
#include "fdb.h"

int main( int argc, char **argv )
{
  iformat idata;
  fdb_t *table;
  FILE *ifh;
  uint i, j, k;
  get_fdb( table );
  ifh = fopen( "../landscape.nod", "rb" );
  if( ifh == NULL )
    return EXIT_FAILURE;
  parse_iformat( ifh, &idata, table );
  fclose( ifh );
  dump_iformat( &idata );
  for( i = 0; i < idata.sets; i++ )
    for( j = 0; j < idata.set[ i ].epochs; j++ )
      for( k = 0; k < idata.set[ i ].signals; k++ )
	{
	  see( idata.layer, idata.set[ i ].signal[ k ].in );
	  think( &idata.layer[ 1 ], idata.dlayers );
	  if( idata.op > 0 )
	    learn( idata.layer,
		   idata.dlayers,
		   idata.set[ i ].signal[ k ].out );
	}
  return EXIT_SUCCESS;
}
