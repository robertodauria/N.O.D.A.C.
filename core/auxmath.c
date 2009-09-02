#include <math.h>
#include "auxmath.h"

float idem( float x )
{
  return x;
}

float flat( float x )
{
  return 1.0;
}

float tanhf_d( float x )
{
  return powf( cosh(x), -2.0 );
}
