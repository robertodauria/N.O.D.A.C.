#ifndef FDB_H
#define FDB_H

typedef struct
{
  float (*function)( float x );
  float (*derivative)( float x );
} fdb_t;

void get_fdb( fdb_t *fdb );

#endif // FDB_H
