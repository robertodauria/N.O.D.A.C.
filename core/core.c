#include <stdio.h>
#include <stdlib.h>
#include "core.h"
#include "parsing.h"
#include "tracing.h"
#include "computing.h"
#include "fdb.h"

int main( int argc, char **argv )
{
  format_t idata;
  fdb_t *table;
  FILE *fh;
  float eqm = 0;
  float *in;
  int i, j, k;
  set_fdb( &table );
  fh = fopen( "../landscape.nod", "rb" );
  if( fh == NULL )
    return EXIT_FAILURE;
  parse_iformat( fh, &idata, table );
  fclose( fh );
  dump_format( &idata );
  if( idata.op > 0 )
    for( i = 0; i < idata.sets; i++ )
      {
	for( j = 0; j < idata.set[ i ].epochs; j++ )
	  for( k = 0; k < idata.set[ i ].signals; k++ )
	    {
	      see( idata.layer, idata.set[ i ].signal[ k ].in );
	      think( idata.layer, idata.dlayers );
	      learn( idata.layer,
		     idata.dlayers,
		     idata.lr,
		     idata.m,
		     idata.set[ i ].signal[ k ].out,
		     &eqm );
	    }
	dump_eqm( eqm );
      }
  else
    {
      i = idata.layer[ 0 ].neurons;
      in = malloc( i * sizeof( float ) );
      while( fread( in, sizeof( float ), i, stdin ) == (size_t) i )
	{
	  see( idata.layer, in );
	  think( &idata.layer[ 1 ], idata.dlayers );
	  fh = fopen( "../landscape.out", "wb" );
	  if( fh == NULL )
	    return EXIT_FAILURE;
	  dump_memory( fh, &idata, table );
	  fclose( fh );
	  dump_output( &idata.layer[ idata.dlayers ] );
	}
      free( in );
    }
  return EXIT_SUCCESS;
}
