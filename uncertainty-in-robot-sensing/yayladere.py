walls="x xx  xx x"
sensors=["on","on","off","on"]

# your code starts

col_num = len(walls)
time = len(sensors)

on_given_wall = 0.7
off_given_wall = 0.3
on_given_no_wall = 0.2
off_given_no_wall = 0.8

right_in_even = 0.8
stay_in_even = 0.2
right_in_odd = 0.6
stay_in_odd = 0.4

# Initialize the probability of being in each position at any time to equal probabilities
robot_loc_prob_over_time = [[1/col_num for col in range(col_num)] for t in range(time+1)]

def normalize (arr):
    sum = 0
    for item in arr:
        sum += item

    for i in range(len(arr)):
        arr[i] = arr[i]/sum
    
    return arr

# Iterate over each time step
for t in range(1, time+1):

    # Iterate over each position
    for col in range(col_num):

        # Calculate the emission probabilities
        if sensors[t-1] == "on":
            if walls[col] == "x":
                robot_loc_prob_over_time[t - 1][col] = robot_loc_prob_over_time[t - 1][col] * on_given_wall;
            else:
                robot_loc_prob_over_time[t - 1][col] = robot_loc_prob_over_time[t - 1][col] * on_given_no_wall;
        if sensors[t-1] == "off":
            if walls[col] == "x":
                robot_loc_prob_over_time[t - 1][col] = robot_loc_prob_over_time[t - 1][col] * off_given_wall;
            else:
                robot_loc_prob_over_time[t - 1][col] = robot_loc_prob_over_time[t - 1][col] * off_given_no_wall;
        
         # Calculate the transition probabilities
        if col == 0: # first index, odd
            robot_loc_prob_over_time[t][col] = robot_loc_prob_over_time[t - 1][col] * stay_in_odd
        elif col == col_num - 1: # last index
            if col % 2 == 0: # odd col
                robot_loc_prob_over_time[t][col] = robot_loc_prob_over_time[t - 1][col - 1] * right_in_even + robot_loc_prob_over_time[t - 1][col] 
            else:  # even col
                robot_loc_prob_over_time[t][col] = robot_loc_prob_over_time[t - 1][col - 1] * right_in_odd + robot_loc_prob_over_time[t - 1][col] 
        elif col % 2 == 0: # odd col
            robot_loc_prob_over_time[t][col] = robot_loc_prob_over_time[t - 1][col - 1] * right_in_even + robot_loc_prob_over_time[t - 1][col] * stay_in_odd
        else: # even col
            robot_loc_prob_over_time[t][col] = robot_loc_prob_over_time[t - 1][col - 1] * right_in_odd + robot_loc_prob_over_time[t - 1][col] * stay_in_even 

    robot_loc_prob_over_time[t] = normalize(robot_loc_prob_over_time[t])

robot_pos_prob = max(robot_loc_prob_over_time[time])
robot_pos = robot_loc_prob_over_time[time].index(robot_pos_prob) + 1

# your code ends

print('The most likely current position of the robot is',robot_pos,'with probability',robot_pos_prob)