/*
 * curves.cpp
 *
 *  Created on: Aug 12, 2020
 *      Author: Paarm Dsehpande
 */




/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "../Inc/global.h"
#include "../Inc/curves.h"

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN TD */


struct Curves area,roll,pitch,yaw;
//.test = 10;
/* USER CODE END TD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */
#define getCurveVal(x,d,c,b,a) (d*pow(x,3) + c*pow(x,2) + b*pow(x,1) + a)
/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
/* USER CODE BEGIN PV */
static const byte  startMarker[] = "<";
static const byte  endMarker[] = ">";
static const byte  delimiter[] =",";
static const byte  semicolonDelim[] =";";
static bool parse_entered_once = FALSE;
static byte* saveptr1; 
static byte* saveptr2; 
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code x---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/* External variables --------------------------------------------------------*/
/* USER CODE BEGIN EV */
/* USER CODE END EV */


void parseData(byte * parseMsg){
  saveptr1 = NULL;  
  saveptr2 = NULL; 
  int frameIndex = 0;
  byte* frameToken = strtok_r(parseMsg,(byte *)semicolonDelim,&saveptr1);
    
  parseCoeffs(frameToken,frameIndex);
  while (frameToken != NULL){
    ++frameIndex;
	  frameToken = strtok_r(NULL, (byte *)semicolonDelim,&saveptr1);
    if(frameToken!=NULL){
      parseCoeffs(frameToken,frameIndex);
    }
  }
}

/**
  * @brief This function handles Hard fault interrupt.
  */
void parseCoeffs(byte * frameMsg, int index){
  byte * coeffsToken = strtok_r(frameMsg,(byte*) delimiter, &saveptr2);

  area.curves[index].d = atof(coeffsToken);
  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  area.curves[index].c = atof(coeffsToken);
  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  area.curves[index].b = atof(coeffsToken);
  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  area.curves[index].a = atof(coeffsToken);
  
  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  roll.curves[index].d = atof(coeffsToken);
  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  roll.curves[index].c = atof(coeffsToken);
  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  roll.curves[index].b = atof(coeffsToken);
  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  roll.curves[index].a = atof(coeffsToken);

  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  pitch.curves[index].d = atof(coeffsToken);
  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  pitch.curves[index].c = atof(coeffsToken);
  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  pitch.curves[index].b = atof(coeffsToken);
  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  pitch.curves[index].a = atof(coeffsToken);

  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  yaw.curves[index].d = atof(coeffsToken);
  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  yaw.curves[index].c = atof(coeffsToken);
  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  yaw.curves[index].b = atof(coeffsToken);
  coeffsToken = strtok_r(NULL,(byte*) delimiter, &saveptr2);
  yaw.curves[index].a = atof(coeffsToken);

}
