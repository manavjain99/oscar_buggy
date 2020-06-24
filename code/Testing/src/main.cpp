#include <Arduino.h>
#include "stm32f4xx_hal.h"
/*
  Timebase callback
  This example shows how to configure HardwareTimer to execute a callback at regular interval.
  Callback toggles pin.
  Once configured, there is only CPU load for callbacks executions.
*/

//void SystemClockConfig(void);
void TIMER5_Init(void);
//void GPIO_Init(void);
void Error_handler(void);

TIM_HandleTypeDef htimer5;

#if defined(LED_BUILTIN)
#define pin  LED_BUILTIN
#else
#define pin  D2
#endif


void TIMER5_Init(void)
{
	htimer5.Instance = TIM5;
	htimer5.Init.Prescaler = 24;
	htimer5.Init.Period = 64000-1;
	if( HAL_TIM_Base_Init(&htimer5) != HAL_OK )
	{
		Error_handler();
	}

}

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
	//HAL_GPIO_TogglePin(GPIOA,GPIO_PIN_5);
  digitalWrite(pin, !digitalRead(pin));

}
HAL_TIM_Base_Start_IT(&htim5);

void Error_handler(void)
{
	while(1);
}


void setup(){
  HAL_Init();
	//SystemClockConfig();
	//GPIO_Init();
	TIMER5_Init();

	//Lets start timer in IT mode
	HAL_TIM_Base_Start_IT(&htimer5);
}


void loop()
{
  /* Nothing to do all is done by hardware. Even no interrupt required. */
  //digitalWrite(pin, !digitalRead(pin));
  
}