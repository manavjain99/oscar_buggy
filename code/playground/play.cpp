#include<iostream>
#include<cmath>

#define RETURN_MAX(x,y) ((abs(x)>y) ? ((x>0)?(y):(-y)) : (x)  )

int main(){
std::cout << RETURN_MAX(6,4) << std::endl;
return 0;
}