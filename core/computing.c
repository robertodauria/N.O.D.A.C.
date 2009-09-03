#include <math.h>
#include "computing.h"
#include "core.h"

void see( layer_t *layer, const float *signal )
{
  int i;
  for( i = 0; i < layer->neurons; i++ )
    layer->neuron[ i ].activation
      = layer->activation->function( signal[ i ] );
}

void think( layer_t *layer, uint dlayers )
{
  int i, j;
  float signal;
  for( i = 1; i < dlayers; i++ )
    for( j = 0; j < layer[ i ].neurons; j++ )
      {
	signal = collect( &layer[ i - 1 ], j );
	layer[ i ].neuron[ j ].activation
	  = layer[ i ].activation->function( signal );
      }
}

void learn( layer_t *layer,
	    const uint dlayers,
	    const float lr,
	    const float m,
	    const float *expected,
	    float *eqm )
{
  int i, j, k;
  float new_change, act;
  for( i = 0; i < layer[ dlayers ].neurons; i++ )
    {
      act = layer[ dlayers ].neuron[ i ].activation;
      *eqm += 0.5 * pow( ( expected[ i ] - act ), 2.0 );
      layer[ dlayers ].neuron[ i ].delta
	= layer[ dlayers ].activation->derivative( act )
	* ( expected[ i ] - act );
      new_change = act * layer[ dlayers ].neuron[ i ].delta;
      *layer[ dlayers ].neuron[ i ].weigth += lr * new_change
	+ m * layer[ dlayers ].neuron[ i ].change;
      layer[ dlayers ].neuron[ i ].change = new_change;
    }
  for( i = dlayers - 1; i >= 0 ; i-- )
    for( j = 0; j < layer[ i ].neurons; j++ )
      for( k = 0; k < layer[ i + 1 ].neurons; k++ )
	{
	  layer[ i ].neuron[ j ].delta
	    += layer[ i + 1 ].neuron[ j ].delta
	    * layer[ i ].neuron[ j ].weigth[ k ];
	  new_change = layer[ i ].neuron[ j ].activation
	    * layer[ i ].neuron[ j ].delta;
	  layer[ i ].neuron[ j ].weigth[ k ]
	    += lr * new_change + m * layer[ i ].neuron[ j ].change;
	  layer[ i ].neuron[ j ].change = new_change;
	}
}

float collect( const layer_t *layer, uint level )
{
  int i;
  float signal = 0;
  for( i = 0; i < layer->neurons; i++ )
    signal
      += layer->neuron[ i ].activation
      * layer->neuron[ i ].weigth[ level ];
  return signal;
}
