/*
 * buggy.c
 *
 *  Created on: Sep 22, 2020
 *      Author: deshp
 */


#include "../Inc/main.h"
#include "../Inc/global.h"
#include "../Inc/buggy.h"
#include "../Inc/gimbal_stuff.h"
#include "../Inc/curves.h"


#define LONG_IP1_PORT GPIOB
#define LONG_IP1_PIN GPIO_PIN_1
#define LONG_IP2_PORT GPIOB
#define LONG_IP2_PIN GPIO_PIN_15

#define LAT_IP1_PORT GPIOB
#define LAT_IP1_PIN GPIO_PIN_14
#define LAT_IP2_PORT GPIOB
#define LAT_IP2_PIN GPIO_PIN_13

extern TIM_HandleTypeDef htim3;
extern TIM_HandleTypeDef htim4;

/*Tim3 ch4 LONGITUDINAL PWM*/
/*Tim4 ch3 LATERAL PWM*/

/* < 0 Motors backward , > 0 Motors Forward, mod(PercentPWM)<=100 */
void longMotn(int8_t PercentPWM ){
	if(PercentPWM > 100 || PercentPWM < -100){
		Error_Handler();
	}
	if(PercentPWM > 0){
		__HAL_TIM_SetCompare(&htim3, TIM_CHANNEL_4, ((float_t)PercentPWM*htim3.Init.Period)/(100.0F)); //update pwm value
		HAL_GPIO_WritePin(LONG_IP1_PORT, LONG_IP1_PIN, SET);
		HAL_GPIO_WritePin(LONG_IP2_PORT, LONG_IP2_PIN, RESET);
	}
    else if(PercentPWM < 0){
        __HAL_TIM_SetCompare(&htim3, TIM_CHANNEL_4, ((float_t)(-PercentPWM)*htim3.Init.Period)/(100.0F)); //update pwm value
		HAL_GPIO_WritePin(LONG_IP1_PORT, LONG_IP1_PIN, RESET);
		HAL_GPIO_WritePin(LONG_IP2_PORT, LONG_IP2_PIN, SET);
    }
    else if(PercentPWM == 0){
        HAL_GPIO_WritePin(LONG_IP1_PORT, LONG_IP1_PIN, RESET);
		HAL_GPIO_WritePin(LONG_IP2_PORT, LONG_IP2_PIN, RESET);
    }
}
/*<0 motor steer Left , > 0 motor steer Right, mod(PercentPWM)<=100 */
void lateralMotn(int8_t PercentPWM ){
	if(PercentPWM > 100 || PercentPWM < -100){
		Error_Handler();
	}
	if(PercentPWM > 0){
		__HAL_TIM_SetCompare(&htim4, TIM_CHANNEL_3, ((float_t)PercentPWM*htim3.Init.Period)/(100.0F)); //update pwm value
		HAL_GPIO_WritePin(LAT_IP1_PORT, LAT_IP1_PIN, SET);
		HAL_GPIO_WritePin(LAT_IP2_PORT, LAT_IP2_PIN, RESET);
	}
    else if(PercentPWM < 0){
        __HAL_TIM_SetCompare(&htim4, TIM_CHANNEL_3, ((float_t)(-PercentPWM)*htim3.Init.Period)/(100.0F)); //update pwm value
		HAL_GPIO_WritePin(LAT_IP1_PORT, LAT_IP1_PIN, RESET);
		HAL_GPIO_WritePin(LAT_IP2_PORT, LAT_IP2_PIN, SET);
    }
    else if(PercentPWM == 0){
        HAL_GPIO_WritePin(LAT_IP1_PORT, LAT_IP1_PIN, RESET);
		HAL_GPIO_WritePin(LAT_IP2_PORT, LAT_IP2_PIN, RESET);
    }
}
