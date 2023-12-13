import tkinter as tk
import random
import math

class Particle:
    global_best = [float('inf'), float('inf')]
    
    def __init__(self, canvas, x, y, is_goal=False):
        self.canvas = canvas
        if is_goal:
            self.id = canvas.create_oval(x, y, x+20, y+20, fill="red")
        else:
            self.id = canvas.create_oval(x, y, x+3, y+3, fill="black")
        self.x = x
        self.y = y
        self.is_goal = is_goal
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.personal_best = [x, y]  # Initialize personal_best with the current position

    def move_towards(self, goal_x, goal_y, w, c1, c2):
        if not self.is_goal:
            r1, r2 = random.random(), random.random()

            # Calculate distance from the goal for both current and personal_best positions
            current_distance = math.sqrt((self.x - goal_x)**2 + (self.y - goal_y)**2)
            personal_best_distance = math.sqrt((self.personal_best[0] - goal_x)**2 + (self.personal_best[1] - goal_y)**2)
            global_best_distance = math.sqrt((Particle.global_best[0] - goal_x)**2 + (Particle.global_best[1] - goal_y)**2)

            # Update personal_best if the current position is closer to the goal
            if current_distance < personal_best_distance:
                self.personal_best = [self.x, self.y]
            
             # Update global_best if the personal_best is closer
            if personal_best_distance < global_best_distance:
                Particle.global_best = self.personal_best

            # Update velocity using the equation
            self.velocity[0] = w * self.velocity[0] + c1 * r1 * (self.personal_best[0] - self.x) + c2 * r2 * (Particle.global_best[0] - self.x)
            self.velocity[1] = w * self.velocity[1] + c1 * r1 * (self.personal_best[1] - self.y) + c2 * r2 * (Particle.global_best[1] - self.y)

            self.x += self.velocity[0]
            self.y += self.velocity[1]

            self.canvas.coords(self.id, self.x, self.y, self.x + 3, self.y + 3)

class PSOApp:
    def __init__(self, master):
        self.master = master
        master.title("PSO Visualization")
        master.state('zoomed')

        # Frame for PSO Parameters
        self.param_frame = tk.Frame(master)
        self.param_frame.pack(pady=5, padx=10, side=tk.LEFT)

        self.num_particles_label = tk.Label(self.param_frame, text="Number of Particles:")
        self.num_particles_label.grid(row=0, column=0, pady=5)
        self.num_particles_entry = tk.Entry(self.param_frame)
        self.num_particles_entry.grid(row=0, column=1, pady=5)

        self.w_label = tk.Label(self.param_frame, text="Inertia Weight (w):")
        self.w_label.grid(row=1, column=0, pady=5)
        self.w_entry = tk.Entry(self.param_frame)
        self.w_entry.grid(row=1, column=1, pady=5)

        self.c1_label = tk.Label(self.param_frame, text="C1:")
        self.c1_label.grid(row=2, column=0, pady=5)
        self.c1_entry = tk.Entry(self.param_frame)
        self.c1_entry.grid(row=2, column=1, pady=5)

        self.c2_label = tk.Label(self.param_frame, text="C2:")
        self.c2_label.grid(row=3, column=0, pady=5)
        self.c2_entry = tk.Entry(self.param_frame)
        self.c2_entry.grid(row=3, column=1, pady=5)

        self.goal_x_label = tk.Label(self.param_frame, text="Goal X: (1-959)")
        self.goal_x_label.grid(row=4, column=0, pady=5)
        self.goal_x_entry = tk.Entry(self.param_frame)
        self.goal_x_entry.grid(row=4, column=1, pady=5)

        self.goal_y_label = tk.Label(self.param_frame, text="Goal Y: (1-639)")
        self.goal_y_label.grid(row=5, column=0, pady=5)
        self.goal_y_entry = tk.Entry(self.param_frame)
        self.goal_y_entry.grid(row=5, column=1, pady=5)

        self.start_button = tk.Button(self.param_frame, text="Start", command=self.start_simulation)
        self.start_button.grid(row=7, column=1)

        # Set initial values
        self.w_entry.insert(0, "0.5")
        self.c1_entry.insert(0, "2")
        self.c2_entry.insert(0, "2")
        self.num_particles_entry.insert(0, "35")
        self.goal_x_entry.insert(0, "700")
        self.goal_y_entry.insert(0, "450")

        # Canvas for drawing
        self.canvas = tk.Canvas(master, width=960, height=640, bg="white")
        self.canvas.pack(padx=10, side=tk.RIGHT)

        self.particles = []

    def start_simulation(self):
        self.start_button.config(state=tk.DISABLED)

        goal_x = float(self.goal_x_entry.get())
        goal_y = float(self.goal_y_entry.get())
        w = float(self.w_entry.get())
        c1 = float(self.c1_entry.get())
        c2 = float(self.c2_entry.get())
        num_particles = int(self.num_particles_entry.get())

        self.goal_particle = Particle(self.canvas, goal_x, goal_y, is_goal=True)

        # Create particles with initial positions forming a circle around the swarm center
        swarm_center_x = 75
        swarm_center_y = 75
        circle_radius = 100
        for i in range(num_particles):
            angle = (2 * math.pi / num_particles) * i
            x = swarm_center_x + circle_radius * math.cos(angle)
            y = swarm_center_y + circle_radius * math.sin(angle)
            particle = Particle(self.canvas, x, y)
            self.particles.append(particle)

        # Animation loop
        self.animate_particles(goal_x, goal_y, w, c1, c2)

    def animate_particles(self, goal_x, goal_y, w, c1, c2):
        if all(self.is_particle_at_goal(p, goal_x, goal_y) for p in self.particles):
            return

        for particle in self.particles:
            particle.move_towards(goal_x, goal_y, w, c1, c2)

        self.master.update()
        self.master.after(250, lambda: self.animate_particles(goal_x, goal_y, w, c1, c2))

    @staticmethod
    def is_particle_at_goal(particle, goal_x, goal_y):
        distance = math.sqrt((particle.x - goal_x)**2 + (particle.y - goal_y)**2)
        return distance < 10

if __name__ == "__main__":
    root = tk.Tk()
    app = PSOApp(root)
    root.mainloop()