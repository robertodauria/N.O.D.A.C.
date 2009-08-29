#ifndef CORE_H
#define CORE_H

typedef unsigned int uint;

typedef struct
{
  float activation;
  float *weigth;
  float *change;
} neuron_t;

typedef struct
{
  uint neurons;
  uint activation;
  neuron_t *neuron;
} layer_t;

typedef struct
{
  float *in;
  float *out;
} signal_t;

typedef struct
{
  uint epochs;
  uint signals;
  signal_t *signal;
} set_t;

typedef struct
{
  uint version;
  uint dlayers;
  layer_t *layer;
  float *memory;
  uint op;
  float lr;
  float m;
  uint sets;
  set_t *set;
} iformat;

#endif // CORE_H
