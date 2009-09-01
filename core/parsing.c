#include <stdio.h>
#include <stdlib.h>
#include "parsing.h"
#include "core.h"

void parse_iformat( FILE *input, iformat *data, const fdb_t *table )
{
  uint i, j;
  uint synapsis;
  rewind( input );
  fread( &data->version, sizeof( uint ), 1, input );
  fread( &data->dlayers, sizeof( uint ), 1, input );
  data->layer = malloc( ( data->dlayers + 1 ) * sizeof( layer_t ) );
  for( i = 0; i <= data->dlayers; i++ )
    {
      fread( &data->layer[ i ].neurons, sizeof( uint ), 1, input );
      fread( &j, sizeof( uint ), 1, input );
      data->layer[ i ].activation = &table[ j ];
    }
  for( i = 0; i < data->dlayers; i++ )
    {
      synapsis = data->layer[ i + 1 ].neurons;
      data->layer[ i ].neuron
	= malloc( data->layer[ i ].neurons * sizeof( neuron_t ) );
      for( j = 0; j < data->layer[ i ].neurons; j++ )
	{
	  data->layer[ i ].neuron[ j ].weigth
	    = malloc( synapsis * sizeof( float ) );
	  fread( data->layer[ i ].neuron[ j ].weigth,
		 sizeof( float ),
		 synapsis,
		 input );
	  data->layer[ i ].neuron[ j ].change
	    = calloc( synapsis, sizeof( float ) );
	}
    }
  data->layer[ data->dlayers ].neuron
    = malloc( data->layer[ data->dlayers ].neurons * sizeof( neuron_t ) );
  for( j = 0; j < data->layer[ data->dlayers ].neurons; j++ )
    {
      data->layer[ data->dlayers ].neuron[ j ].weigth
	= malloc( sizeof( float ) );
      fread( data->layer[ data->dlayers ].neuron[ j ].weigth,
	     sizeof( float ),
	     1,
	     input );
    }
  fread( &data->op, sizeof( uint ), 1, input );
  fread( &data->lr, sizeof( float ), 1, input );
  fread( &data->m, sizeof( float ), 1, input );
  fread( &data->sets, sizeof( uint ), 1, input );
  data->set = malloc( data->sets * sizeof( set_t ) );
  for( i = 0; i < data->sets; i++ )
    {
      fread( &data->set[ i ].epochs, sizeof( uint ), 1, input );
      fread( &data->set[ i ].signals, sizeof( uint ), 1, input );
      data->set[ i ].signal
	= malloc( data->set[ i ].signals * sizeof( signal_t ) );
      for( j = 0; j < data->set[ i ].signals; j++ )
	{
	  data->set[ i ].signal[ j ].in
	    = malloc( data->layer[ 0 ].neurons * sizeof( float ) );
	  fread( data->set[ i ].signal[ j ].in,
		 sizeof( float ),
		 data->layer[ 0 ].neurons,
		 input );
	  data->set[ i ].signal[ j ].out
	    = malloc( data->layer[ data->dlayers ].neurons * sizeof( float ) );
	  fread( data->set[ i ].signal[ j ].in,
		 sizeof( float ),
		 data->layer[ data->dlayers ].neurons,
		 input );
	}
    }
}
