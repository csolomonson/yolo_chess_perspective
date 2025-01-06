# chessMove.py
#
# Expected input: startPosition, endPosition, occupied
#   startPosition = [A-H][1-8]
#   endPosition = [A-H][1-8]
#   occupied = [True|False] (Is the endPosition occupied?)
#
# Example: A2, C3, False


# Standard Modules
import sys
import math
from time import sleep

# Installed Modules
import rtde_control
import rtde_receive
import rtde_io

# Custom Modules
import board # Position Values
#from button_utils import wait_for_gripper

# Variables
#==============================================================================
#robotIP = "172.20.92.238"
robotIP = "10.30.21.100"

dropdist = 0.077 # meters of drop and pick

# Modes
#==============================================================================
WAIT_FOR_IN = True

# Initialization
#==============================================================================
rtde_c = rtde_control.RTDEControlInterface(robotIP)
rtde_r = rtde_receive.RTDEReceiveInterface(robotIP)
rtde_io = rtde_io.RTDEIOInterface(robotIP)

rtde_c.setPayload(1.330,[.009,.007,.039])

rtde_io.setStandardDigitalOut(5, False)



# Functions
#==============================================================================
def JointRad(lstDegree):
    '''
    Convert the joint angles from degrees to radians
    '''
    lstRad = [math.radians(i)for i in lstDegree]
    return lstRad


def pick(position, board=board):
    '''
    Go to a position with an empty gripper, go down, close the gripper, and go up.
    '''
    print ("Moving to {}".format(position))
    lstJoints = getattr(board, position)
    rtde_c.moveJ(JointRad(lstJoints), 0.5, 0.3)
    target = rtde_r.getActualTCPPose()
    target[2] -= dropdist
    rtde_c.moveL(target) #drop
    sleep(1)
    rtde_io.setStandardDigitalOut(5, True)
    sleep(1)
    
    target[2] += dropdist
    rtde_c.moveL(target) #pick

def drop(position, board=board):
    '''
    Go to a position with a full gripper, go down, release the piece, and go up.
    '''
    print ("Moving to {}".format(position))
    lstJoints = getattr(board, position)
    rtde_c.moveJ(JointRad(lstJoints), 0.5, 0.3)
    target = rtde_r.getActualTCPPose()
    target[2] -= dropdist
    rtde_c.moveL(target) #drop
    sleep(1)
    rtde_io.setStandardDigitalOut(5, False)
    sleep(1)
    target[2] += dropdist
    rtde_c.moveL(target) #pick


def drop_capture():
    '''
    When a piece is captured, the robot picks up the piece to capture, drops it in a discard location, and then moves the capturing piece.
    This method drops whatever is in the gripper at the discard location, specified in board.py.
    '''
    lstJoints = getattr(board, 'CAPTURE')
    rtde_c.moveJ(JointRad(lstJoints), 0.5, 0.3)
    rtde_io.setStandardDigitalOut(5, False)





def move(startPosition, endPosition, occupied=True):
    '''
    If the target space is occupied, then this must be a capture. In that case, pick up the piece to be captured, drop it in the discard location, and then move the capturing piece
    If the target space is not occupied, simply move the piece to its new position.
    '''
    print('Moving from {} to {}'.format(startPosition, endPosition))
    if occupied:
        pick(endPosition)
        drop_capture()
    pick(startPosition)
    drop(endPosition)



# Interactive from Command Line
#==============================================================================

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Expecting 3 arguements')
    else:
        startPosition = sys.argv[1].upper()
        endPosition = sys.argv[2].upper()
        occupied = sys.argv[3]

        move(startPosition, endPosition, occupied)

        # print('{} {} {}'.format(startPosition, endPosition, occupied))

    
