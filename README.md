# oscar_buggy

Bare minimum aim : To track a static football according to the director module.

Project currently in the initial phase of development, done with simulation and testing of YOLO algorithm and stanley controller on the Carla simulator.

## Notes

### For gimbal 

        +ve | -ve                   +ve
            |                   -----------          havent really used ROLL.
            |                       -ve

        yaw (TOPVIEW)          pitch (FRONTVIEW)


    The vals are inverted for obcomp/camera during processing. Make sure to invert them before sending.
