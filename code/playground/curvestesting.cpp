/*
 * curves.cpp
 *
 *  Created on: Aug 12, 2020
 *      Author: Paarm Dsehpande
 */




/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/


/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <stdbool.h>
#include <string.h>
#include <cmath>
#include <iostream>

using namespace std;
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN TD */

#define MAXCURVES 15
typedef char byte;
struct curve
{
  /* data */
  int16_t d;
  int16_t c;
  int16_t b;
  int16_t a;

};

struct Curves{
	struct curve curves[MAXCURVES];
};

Curves area,roll,pitch,yaw;
//.test = 10;
/* USER CODE END TD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
void parseCoeffs(byte * frameMsg, int );
void parseData(byte * );
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

/**
  * @brief This function handles Hard fault interrupt.
  */
void parseData(byte * parseMsg){
  byte* frameToken = strtok_r(parseMsg,(byte *)startMarker,&saveptr1);
  frameToken = strtok_r(NULL,(byte *)endMarker,&saveptr1); // Now it points to the first frame.
  cout << "token is:" << frameToken << endl;
  int frameIndex = 0;
  byte* frameTokenCopy = frameToken;
  parseCoeffs(frameTokenCopy,frameIndex);
  while (frameToken != NULL){
    /* code */
    cout << "insidewhile" << endl;

    frameToken = strtok_r(NULL, (byte *)startMarker,&saveptr1);
    cout << "retryparse, token should be null is:" << frameToken << endl;
    if(frameToken == NULL){
        cout << "tokennullstart";
    }
    
    frameToken = strtok_r(NULL, (byte *)endMarker,&saveptr1);
    cout << "retryparse, token 2 is:" << frameToken << endl;
        if(frameToken == NULL){
        cout << "tokennullend";
    }
    
    if(frameToken!=NULL){
        cout << "parsing" << endl;
        parseCoeffs(frameToken,frameIndex);
    }
    
    ++frameIndex;
  }
    
}

// Sending <hi>
void parseHi(byte* parseMsg){
    cout << "reached here begin" << endl;
    byte* frameToken = strtok(parseMsg,(byte *)startMarker);
    cout << "Frame token is:" << frameToken <<  endl;
    frameToken = strtok(NULL,(byte *)endMarker); // Now it points to the first frame.
    cout << "reached here end" << endl;
    cout << "Frame token is:" << frameToken <<  endl;
    
}

/**
  * @brief This function handles Hard fault interrupt.
  */
void parseCoeffs(byte * frameMsg, int index){
  byte * coeffsToken = strtok_r(frameMsg,(byte*) delimiter, &saveptr2);
  cout << "Coeff token is:" << coeffsToken << endl;
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
  cout << "Coeff token is:" << coeffsToken << endl;
  yaw.curves[index].a = atof(coeffsToken);

}


int main(){
    char testMsg[] = " <0.0,	 0.0,	 0.0,	 3.990,	 0.0,	 0.0,	 0.0,	 0.0,	 -0.018865938725497182,	 0.0679173794117895,	 -0.6696188776226956,	 3.6917098445595853,	 -0.019224606762103857,	 0.06920858434357391,	 -0.03377792101544628,	 -18.6139896373057 > <	 0.0,	 0.0,	 0.0,	 0.0,	 0.0,	 0.0,	 0.0,	 0.0,	 0.004232282831955581,	 1.1275702593849246e-17,	 0.03708340564080967,	 4.650259067357513,	 -0.04461830375383687,	 0.0,	 0.366495607837304,	 -3.691709844559585>";
    
    parseData((byte*)testMsg);
    char hiMsg[] = " <hi>";
    char* hiptr = hiMsg;
    //parseHi(hiptr);
    cout << "area curves is" << area.curves[0].a ; 
    return 0;
}