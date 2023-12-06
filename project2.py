import sys
import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
import pycuda.gpuarray as gpuarray
from pycuda.compiler import SourceModule
import random
import csv
import ipdb

# Constants
GRID_SIZE = 13

#ipdb.set_trace()
# Create a grid with a fence and an exit
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.int32)

# Create a fence around the perimeter
grid[[0, -1], :] = 1
grid[:, [0, -1]] = 1

# Place the exit randomly on the fence top or bottom, ignoring the extreme corners
exit_position = (random.randint(1, GRID_SIZE - 2), random.choice([0, GRID_SIZE - 1]))
grid[exit_position[0], exit_position[1]] = 2  # Creates Exit at the top or bottom edge coordinates y and x respectively (don't know why it's in that order ask kelvin)

# CUDA kernel for moving goats towards the exit
mod = SourceModule("""
    __global__ void move_towards_exit(int* grid, int* positions, int* positionsPrev, int randDir, int num_Goat, int GRID_SIZE, int exit_x) { //handles parralel goat movement and handles collisons then passes back the updated grid goat positions and previous goat positions to the host
        int tid = threadIdx.x + blockIdx.x * blockDim.x; //blockIdx is the index of the block starting at 0, while the blockDim is the dimension of the block or # of threads in that block which is a constant
        if (tid < num_Goat * 2) {
            int x = tid * 2; //index of specific goat positions actually y coordinate on the grid
            int y = tid * 2 + 1; //the index of a goat's x position on the grid



                if(randDir == 0) { //Move 1 in the right-direction
                positionsPrev[x] = positions[x]; //first update the previous position array with the current positions
                positionsPrev[y] = positions[y];

                positions[x] = positions[x]; //then update the position array with the first try positions
                positions[y] = positions[y] + 1; //y needs to increase here to move goat to the right on the grid because the grid is x = rows(actualycoord), y = columns(actualxcoord)

                    if(grid[(positions[x] * GRID_SIZE) + positions[y]] == 1 || grid[(positions[x] * GRID_SIZE) + positions[y]] == 3){ //Don't move there as that is either a fence, or another goat's fallback position ALSO note that x and y are flipped due to accessing the grid array which is stored flipped
                        positions[x] = positionsPrev[x]; //reset the goat's positions to their previous ones
                        positions[y] = positionsPrev[y];
                    }
                    else{ //update the grid now for ONLY those threads that can move
                        grid[(positions[x] * GRID_SIZE) + positions[y]] = 3; //updates the grid position with a new goat if there was no previous goat last iteration
                        grid[(positionsPrev[x] * GRID_SIZE) + positionsPrev[y]] = 0; //Only sets the goats that moved previous position to 0
                    }

                    //if statement for making sure two goats didn't collide? 3 + 3 = 6
                    //this should never happen because all the goats try to move in the same direction every iteration, so they will never end up moving into the same spot.
                }


                if(randDir == 1) { //Move 1 in the left-direction
                positionsPrev[x] = positions[x];
                positionsPrev[y] = positions[y];

                positions[x] = positions[x];
                positions[y] = positions[y] - 1;

                    if(grid[(positions[x] * GRID_SIZE) + positions[y]] == 1 || grid[(positions[x] * GRID_SIZE) + positions[y]] == 3){ //Don't move there as that is either a fence, or another goat's fallback position
                        positions[x] = positionsPrev[x]; //reset the goat's positions to their previous ones
                        positions[y] = positionsPrev[y];
                    }
                    else{ //update the grid now for ONLY those threads that can move
                        grid[(positions[x] * GRID_SIZE) + positions[y]] = 3; //updates the grid position with a new goat if there was no previous goat last iteration
                        grid[(positionsPrev[x] * GRID_SIZE) + positionsPrev[y]] = 0; //Only sets the goats that moved previous position to 0
                    }
                }


                if(randDir == 2) { //Move 1 in the up direction (-x due to grid)
                positionsPrev[x] = positions[x];
                positionsPrev[y] = positions[y];

                positions[x] = positions[x] - 1;
                positions[y] = positions[y];

                    if(grid[(positions[x] * GRID_SIZE) + positions[y]] == 1 || grid[(positions[x] * GRID_SIZE) + positions[y]] == 3){ //Don't move there as that is either a fence, or another goat's fallback position
                        positions[x] = positionsPrev[x]; //reset the goat's positions to their previous ones
                        positions[y] = positionsPrev[y];
                    }
                    else{ //update the grid now for ONLY those threads that can move
                        grid[(positions[x] * GRID_SIZE) + positions[y]] = 3; //updates the grid position with a new goat if there was no previous goat last iteration
                        grid[(positionsPrev[x] * GRID_SIZE) + positionsPrev[y]] = 0; //Only sets the goats that moved previous position to 0
                    }
                }


                if(randDir == 3) { //Move 1 in the down direction (+x)
                positionsPrev[x] = positions[x];
                positionsPrev[y] = positions[y];

                positions[x] = positions[x] + 1;
                positions[y] = positions[y];

                    if(grid[(positions[x] * GRID_SIZE) + positions[y]] == 1 || grid[(positions[x] * GRID_SIZE) + positions[y]] == 3){ //Don't move there as that is either a fence, or another goat's fallback position
                        positions[x] = positionsPrev[x]; //reset the goat's positions to their previous ones
                        positions[y] = positionsPrev[y];
                    }
                    else{ //update the grid now for ONLY those threads that can move
                        grid[(positions[x] * GRID_SIZE) + positions[y]] = 3; //updates the grid position with a new goat if there was no previous goat last iteration
                        grid[(positionsPrev[x] * GRID_SIZE) + positionsPrev[y]] = 0; //Only sets the goats that moved previous position to 0
                    }
                }

        }

    }
""")



# Create GPU function from the CUDA kernel
move_towards_exit_gpu = mod.get_function("move_towards_exit")


# Goat class
class Goat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xPrev = -100 #start out as placeholder values
        self.yPrev = -100 #start out as placeholder values
        self.collisionCount = 0
        self.exit = False
        grid[self.x][self.y] = 3

    def move_towards_exit(Goat_list): #Needs to pass in the full array of goats, not just one goat because otherwise it would just be using the gpu like the cpu <-----------------------------------------------------------
        # Prepare data for GPU
        positions_host = np.array([], dtype=np.int32) #resets the array so that goat positions are added newly each time, helps with when there is only 1 goat left.
        positionsPrev_host = np.array([], dtype=np.int32) #resets the array so that goat positions are added newly each time, helps with when there is only 1 goat left.

        for x in range(len(Goat_list)):
          positions_host = np.append(positions_host, [Goat_list[x].x, Goat_list[x].y]) #creates an array of positions on the host device of the goat's positions as a signed int
          positionsPrev_host = np.append(positionsPrev_host, [Goat_list[x].xPrev, Goat_list[x].yPrev]) #creates an array of previous positions on the host device of the goat's positions as a signed int

        positions_device = gpuarray.to_gpu(positions_host) #creates a copy of the array from the host on the device and allocates memory on the device automatically
        positionsPrev_device = gpuarray.to_gpu(np.array(positionsPrev_host)) #creates a copy of the previous position array from the host on the device and allocates memory on the device automatically
        grid_device = gpuarray.to_gpu(grid.flatten()) #flattens the 2d grid array of goat positions and fence positions into a 1d position array for easier transfer to gpu can undo with myArray.reshape(rows, columns) later

        # Move Goat towards the exit on GPU
        block_size = 4 #number of rows of threads per block
        grid_size = (num_Goat + block_size - 1) // block_size #number of blocks per Gpu grid

        #get a random direction choice to try first
        trydirection = random.choice([0,1,2,3])

        # Use cuda Stream for asynchronous memory transfer
        stream = cuda.Stream()

        # Launch the gpu kernal handling parrallel goat movement and collsions using the stream
        move_towards_exit_gpu(grid_device, positions_device, positionsPrev_device, np.int32(trydirection), np.int32(num_Goat), np.int32(GRID_SIZE),np.int32(exit_position[1]), block=(block_size, 1, 1), grid=(grid_size, 1), stream=stream)

        # Synchronize the stream to ensure completion so that the gpu completes all of the calculations and then waits for all the goats position vectors to get to the same spot in the calculation so that some goats don't get ahead in the number of iterations over other goats.        stream.synchronize()
        stream.synchronize()

        # Copy updated position data back from GPU asynchronously because some gpu threads can complete faster than others, for example if there are if statements, then the gpu will break up the process and calculate the first half of threads that went one way, and then process the other threads that went the other way. the first set would have already been completed, while the 2nd was still finishing the calculations
        positions_host = positions_device.get(stream=stream)

        # Free GPU memory
        positions_device.gpudata.free()

        # Copy updated previous position data back from GPU
        positionsPrev_host = positionsPrev_device.get(stream=stream)

        # Free GPU memory
        positionsPrev_device.gpudata.free()

        # Copy updated grid data back from GPU
        newGrid = grid_device.get(stream=stream).reshape(GRID_SIZE, GRID_SIZE)

        # Free GPU memory
        grid_device.gpudata.free()

        # Update the Goat objects with the new positions
        for i, goat in enumerate(Goat_list):
            goat.xPrev, goat.yPrev = positionsPrev_host[i * 2], positionsPrev_host[i * 2 + 1]
            goat.x, goat.y = positions_host[i * 2], positions_host[i * 2 + 1]

        return newGrid

    def is_on_exit(self):
        # Check if the Goat is on the exit
        return self.x == exit_position[0] and self.y == exit_position[1] #pos[0] = rows or y values, pos[1] = columns or x values


# Create a list of Goat
num_Goat = 120
Goat_list = []

# List of available goat locations
available_positions = [(x, y) for x in range(1, GRID_SIZE - 1) for y in range(1, GRID_SIZE - 1) if grid[x, y] == 0]

# Ensure you have enough available positions for the desired number of goats
if len(available_positions) < num_Goat:
    raise ValueError("Not enough available positions for goats.")

# Randomly select positions from the available positions
selected_positions = random.sample(available_positions, num_Goat)

# Create Goat objects at the selected positions
for position in selected_positions:
    x, y = position
    Goat_list.append(Goat(x, y))




# Specify the CSV file path
csv_file_path = "GoatOutput.csv"

with open(csv_file_path, mode='w', newline='') as file: #resets the csv file every time the program is run
    writer = csv.writer(file)
    writer.writerow([])

# Function to convert a goat to a CSV string
def goat_to_csv_string(goat, goat_number):
    return [f"Goat ID: {goat}", f"X: {goat.y}", f"Y: {goat.x}", ""]




# Main simulation loop
iteration = 0
csvIteration = 0
csvNumGoat = num_Goat
while num_Goat > 0:
  # printing the list using loop
  #for x in range(len(Goat_list)):
    #print(f"Goat {x}: XCoord: {Goat_list[x].y} YCoord: -{Goat_list[x].x}") #again, y is x and x is y

  iteration += 1

  #QUICK FIX hopefully for the edges turning to 0s randomly, if we find why this happens we can get rid of this...
  # Set edges to 1 where the value is not 2
  grid[0, grid[0, :] != 2] = 1  # Top edge
  grid[-1, grid[-1, :] != 2] = 1  # Bottom edge
  grid[:, 0][grid[:, 0] != 2] = 1  # Left edge
  grid[:, -1][grid[:, -1] != 2] = 1  # Right edge

  # Iterate and continuously append data horizontally
  new_data = []
  for index, goat in enumerate(Goat_list):
    csv_string = goat_to_csv_string(goat, index + 1)
    new_data.append(csv_string)

  iterationData = [["Iteration:", f"{iteration}"]]
  # Append new columns to the CSV file
  with open(csv_file_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(iterationData)
    writer.writerows(map(list, zip(*new_data)))


  # Move Goat towards the exit and check if they are next to it
  print(grid)
  print(f"Exit Position: ({exit_position[1]}, -{exit_position[0]})")
  print(f"Number of Goats: {num_Goat}")
  grid = Goat.move_towards_exit(Goat_list) #passes in the list of goats and returns the updated grid after modifying the goats positions and handling collisions in cuda

  for goat in Goat_list:
    if Goat.is_on_exit(goat):
        Goat_list.remove(goat)
        grid[exit_position] = 2 #resets the grid to have the exit marker
        num_Goat -= 1
        print("removed Goat!")
        print(f"Number of Goats Left: {num_Goat}")

print(grid)
print(f"Number of Goats Left: {num_Goat}")
# Output the number of iterations when all goats have exited
print(f"Done in {iteration} iterations.")
