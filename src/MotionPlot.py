import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Robot class representing the robot in the animation
class Robot:
    def __init__(self, ax):
        self.ax = ax
        self.robot, = ax.plot([], [], 'bo')  # Initialize robot as a blue dot
        self.time_template = 'Time: %.1f s'
        self.time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    def init(self):
        self.robot.set_data([], [])
        self.time_text.set_text('')
        return self.robot, self.time_text

    def update(self, frame):
        # Update robot position in a circular motion
        radius = 5.0
        theta = np.radians(frame)  # Convert frame number to angle in radians
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)

        # Update robot data and time text
        self.robot.set_data(x, y)
        self.time_text.set_text(self.time_template % (frame * 0.1))  # Assuming 1 frame = 0.1 seconds
        return self.robot, self.time_text

# Set up figure and axis
fig, ax = plt.subplots()
ax.set_aspect('equal', 'box')  # Keep the aspect ratio equal for a more realistic view

# Create Robot instance
robot_anim = Robot(ax)

# Set animation interval and number of frames
animation = FuncAnimation(fig, robot_anim.update, frames=100, interval=100, init_func=robot_anim.init, blit=True)

# Display the animation
plt.show()

