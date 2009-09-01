#include "computing.h"
#include "core.h"

void see( layer_t *layer, const float *signal )
{
  uint i;
  for( i = 0; i < layer->neurons; i++ )
    layer->neuron[ i ].activation
      = layer->activation->function( signal[ i ] );
}

void think( layer_t *layer, uint dlayers )
{
  uint i, j;
  float signal;
  for( i = 0; i < dlayers; i++ )
    for( j = 0; j < layer[ i ].neurons; j++ )
      {
	signal = collect( &layer[ i - 1 ], j );
	layer[ i ].neuron[ j ].activation
	  = layer[ i ].activation->function( signal );
      }
}

void learn( layer_t *layer, uint dlayers, const float *expected )
{
  dlayers = 0;
}

float collect( layer_t *layer, uint level )
{
  uint i;
  float signal = 0;
  for( i = 0; i < layer->neurons; i++ )
    signal
      += layer->neuron[ i ].activation * layer->neuron[ i ].weigth[ level ];
  return signal;
}
