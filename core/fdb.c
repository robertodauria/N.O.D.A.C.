#include <math.h>
#include "fdb.h"
#include "core.h"
#include "auxmath.h"

void set_fdb( fdb_t **fdb )
{
  static fdb_t table[] =
    {
      { idem, flat },
      { tanhf, tanhf_d }
    };
  *fdb = table;
}
