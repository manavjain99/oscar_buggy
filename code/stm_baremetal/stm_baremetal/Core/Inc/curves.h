/*
 * curves.h
 *
 *  Created on: Aug 12, 2020
 *      Author: deshp
 */

#ifndef INC_CURVES_H_
#define INC_CURVES_H_



#define MAXCURVES 15
struct curve
{
  /* data */
  float_t d;
  float_t c;
  float_t b;
  float_t a;

};

struct Curves{
	struct curve curves[MAXCURVES];
};

extern struct Curves area,roll,pitch,yaw;

void parseCoeffs(byte* , int );
void parseData(byte * );




#endif /* INC_CURVES_H_ */
