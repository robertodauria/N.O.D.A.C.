#include <stdio.h>
#include "tracing.h"
#include "core.h"

void dump_iformat( const iformat *data )
{
  printf( "Type:\t\t%u\n", data->version );
  printf( "Layers:\t\t%u\n", data->dlayers + 1 );
  printf( "Training mode:\t%u\n", data->op );
  printf( "Learning rate:\t%f\n", data->lr );
  printf( "Momentum:\t%f\n", data->m );
  printf( "Sets:\t\t%u\n", data->sets );
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
