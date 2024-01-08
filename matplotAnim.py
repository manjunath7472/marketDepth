import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from kite_trade import *
import time

with open('enctoken.txt', 'r') as wr:
    token = wr.read()

kite = KiteApp(enctoken=token)

# Common setup
r = 25
v1 = [0 for i in range(1, r)]
v2 = [0 for i in range(1, r)]
v3 = [0 for i in range(1, r)]
x = [i for i in range(1, r)]
  
    
def giveyrange(value):
   
    # Calculating 10% minimum and 10% maximum
    min_value = value * 0.9  # 10% less than the value
    max_value = value * 1.1  # 10% more than the value

    return min_value, max_value

# Function to calculate percentage change
def calculate_percentage_change(current, previous):
    if previous == 0:
        return 0
    pc = ((current - previous) / previous) * 100
    pc = round(pc, 3)
    return pc

# Combined update function
def update_raw_data(frame):
    
    myquote = kite.quote(["NSE:HDFCBANK"])
    v1.append(float(myquote['NSE:HDFCBANK']['buy_quantity']))
    v2.append(float(myquote['NSE:HDFCBANK']['sell_quantity']))
    v3.append(float(myquote['NSE:HDFCBANK']['volume']))
    # Adding new data to each dataset

    # Clear the previous plot
    ax1_raw.clear()
    ax2_raw.clear()
    ax3_raw.clear()

    # Plotting raw data for v1, v2, and v3
    ax1_raw.plot(x, v1[-len(x):], 'green')
    ax1_raw.set_ylabel('v1', color='green')
    ax1_raw.tick_params(axis='y', labelcolor='green')
    ax1_raw.set_ylim(giveyrange((min(v1)+max(v1))/2))

    ax2_raw.plot(x, v2[-len(x):], 'red')
    ax2_raw.set_ylabel('v2', color='red')
    ax2_raw.tick_params(axis='y', labelcolor='red')
    ax2_raw.set_ylim(giveyrange((min(v2)+max(v2))/2))

    ax3_raw.plot(x, v3[-len(x):], 'black')
    ax3_raw.set_ylabel('v3', color='black')
    ax3_raw.tick_params(axis='y', labelcolor='black')
    ax3_raw.set_ylim(giveyrange((min(v3)+max(v3))/2))

# Function to update percentage change
def update_percentage_change(frame):

    # Calculating percentage change for each dataset
    v1_pc = [calculate_percentage_change(v1[i], v1[i-1]) for i in range(1, len(v1))]
    v2_pc = [calculate_percentage_change(v2[i], v2[i-1]) for i in range(1, len(v2))]
    v3_pc = [calculate_percentage_change(v3[i], v3[i-1]) for i in range(1, len(v3))]

    # Clear the previous plot
    ax1_pc.clear()
    ax2_pc.clear()
    ax3_pc.clear()

    # Plotting percentage change for v1, v2, and v3
    ax1_pc.plot(x, v1_pc[-len(x):], 'green')
    ax1_pc.set_ylabel('v1 % Change', color='green')
    ax1_pc.tick_params(axis='y', labelcolor='green')
    ax1_pc.set_ylim(-10, 10)

    ax2_pc.plot(x, v2_pc[-len(x):], 'red')
    ax2_pc.set_ylabel('v2 % Change', color='red')
    ax2_pc.tick_params(axis='y', labelcolor='red')
    ax2_pc.set_ylim(-10, 10)

    ax3_pc.plot(x, v3_pc[-len(x):], 'black')
    ax3_pc.set_ylabel('v3 % Change', color='black')
    ax3_pc.tick_params(axis='y', labelcolor='black')
    ax3_pc.set_ylim(-10, 10)

# Creating two separate figures for raw data and percentage change
fig_raw, ax1_raw = plt.subplots(figsize=(10, 6))
plt.get_current_fig_manager().set_window_title("BSV")
ax2_raw = ax1_raw.twinx()
ax3_raw = ax1_raw.twinx()

fig_pc, ax1_pc = plt.subplots(figsize=(10, 6))
plt.get_current_fig_manager().set_window_title("PercentageChange")
ax2_pc = ax1_pc.twinx()
ax3_pc = ax1_pc.twinx()

# Creating two separate animations
ani_raw = animation.FuncAnimation(fig_raw, update_raw_data, interval=1000)
ani_pc = animation.FuncAnimation(fig_pc, update_percentage_change, interval=1000)

plt.show()