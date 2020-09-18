/*
 * global.h
 *
 *  Created on: Aug 11, 2020
 *      Author: Param Deshpande
 */

#ifndef INC_GLOBAL_H_
#define INC_GLOBAL_H_

#include "main.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <math.h>

#define RXBUFFERSIZE    500
// Each single curveunit is ~250 chars , sending atleast 5 ie 1250chars
#define COMMSBUFFERSIZE 3000

#define TRUE 1
#define FALSE 0

#define AND &&
#define OR ||

#define ITM_Port32(n) (*((volatile unsigned long *)(0xE0000000+4*n)))
typedef char byte;
typedef float float_t;
 
extern UART_HandleTypeDef huart2;
extern UART_HandleTypeDef huart6;

extern uint32_t gimbalHyperframeTime;

#endif /* INC_GLOBAL_H_ */
