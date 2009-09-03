#include <stdio.h>
#include "tracing.h"
#include "core.h"

void dump_format( const format_t *data )
{
  printf( "Type:\t\t%08X\n", data->version );
  printf( "Layers:\t\t%8u\n", data->dlayers + 1 );
  printf( "Training mode:\t%8u\n", data->op );
  printf( "Learning rate:\t%f\n", data->lr );
  printf( "Momentum:\t%f\n", data->m );
  printf( "Sets:\t\t%8u\n\n", data->sets );
}

void dump_eqm( float eqm )
{
  printf( "Error:\t\t%f\n", eqm );
}

void dump_output( const layer_t *last )
{
  uint i;
  printf( "Results:\n" );
  for( i = 0; i < last->neurons; i++ )
    printf( "%-.4u\t%f\n",
	    i,
	    last->neuron[ i ].activation * *last->neuron[ i ].weigth );
}

void dump_memory( FILE *fh, const format_t *data, const fdb_t *table )
{
  int i, j;
  fwrite( &data->version, sizeof( uint ), 1, fh );
  fwrite( &data->dlayers, sizeof( uint ), 1, fh );
  for( i = 0; i <= data->dlayers; i++ )
    {
      fwrite( &data->layer[ i ].neurons, sizeof( uint ), 1, fh );
      j = ( data->layer[ i ].activation - table ) / sizeof( fdb_t );
      fwrite( &j, sizeof( uint ), 1, fh );
    }
  for( i = 0; i < data->dlayers; i++ )
    for( j = 0; j < data->layer[ i ].neurons; j++ )
      fwrite( data->layer[ i ].neuron[ j ].weigth,
	      sizeof( float ),
	      data->layer[ i + 1 ].neurons,
	      fh );
  for( i = 0; i < data->layer[ data->dlayers ].neurons; i++ )
    fwrite( data->layer[ data->dlayers ].neuron[ i ].weigth,
	    sizeof( float ),
	    1,
	    fh );
}
