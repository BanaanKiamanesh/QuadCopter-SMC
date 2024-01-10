import numpy as np
import matplotlib.pyplot as plt


class QuadCopterPlotter:
    def __init__(self, time, states):
        self.time = time
        self.states = states

    def plot_states(self):
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(r'QuadCopter States Over Time',
                     fontsize=16, fontweight='bold')

        # Plot Linear Motion
        axes[0, 0].plot(self.time, self.states[:, 0], label='X')
        axes[0, 0].plot(self.time, self.states[:, 1], label='Y')
        axes[0, 0].plot(self.time, self.states[:, 2], label='Z')
        axes[0, 0].set_title(r'Linear Motion')
        axes[0, 0].set_xlabel(r'Time (s)')
        axes[0, 0].set_ylabel(r'Position')
        axes[0, 0].legend()
        axes[0, 0].grid(True)

        # Plot Angular Motion
        axes[0, 1].plot(self.time, np.degrees(
            self.states[:, 6]), label='Roll ($\phi$)')
        axes[0, 1].plot(self.time, np.degrees(
            self.states[:, 7]), label='Pitch ($\Theta$)')
        axes[0, 1].plot(self.time, np.degrees(
            self.states[:, 8]), label='Yaw ($\Psi$)')
        axes[0, 1].set_title(r'Angular Motion')
        axes[0, 1].set_xlabel(r'Time (s)')
        axes[0, 1].set_ylabel(r'Angle (degrees)')
        axes[0, 1].legend()
        axes[0, 1].grid(True)

        # Additional Plots (modify as needed)
        axes[1, 0].plot(self.time, self.states[:, 3], label='$\dot{X}$')
        axes[1, 0].plot(self.time, self.states[:, 4], label='$\dot{Y}$')
        axes[1, 0].plot(self.time, self.states[:, 5], label='$\dot{Z}$')
        axes[1, 0].set_title(r'Linear Velocities')
        axes[1, 0].set_xlabel(r'Time (s)')
        axes[1, 0].set_ylabel(r'Velocity')
        axes[1, 0].legend()
        axes[1, 0].grid(True)

        axes[1, 1].plot(self.time, np.degrees(self.states[:, 9]),
                        label='Roll Rate ($\dot{\phi}$)')
        axes[1, 1].plot(self.time, np.degrees(self.states[:, 10]),
                        label='Pitch Rate ($\dot{\Theta}$)')
        axes[1, 1].plot(self.time, np.degrees(
            self.states[:, 11]), label='Yaw Rate ($\dot{\Psi}$)')
        axes[1, 1].set_title(r'Angular Velocities')
        axes[1, 1].set_xlabel(r'Time (s)')
        axes[1, 1].set_ylabel(r'Angular Velocity (degrees/s)')
        axes[1, 1].legend()
        axes[1, 1].grid(True)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()


# Example usage:
if __name__ == "__main__":
    # Assuming S and t are obtained from the QuadCopter simulation
    from QuadCopter import QuadCopter
    Quad = QuadCopter()
    S, t = Quad.Simulate(
        x0=[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], t=np.linspace(0, 10, 1000))
    plotter = QuadCopterPlotter(time=t, states=S)
    plotter.plot_states()
