import tkinter as tk
import random
import math

class Particle:
    def __init__(self, canvas_width, canvas_height):
        self.width = canvas_width
        self.height = canvas_height
        
        # Position
        self.x = random.randint(0, canvas_width)
        self.y = random.randint(0, canvas_height)
        
        # Velocity
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-1.5, 1.5)
        
        # Appearance
        self.radius = random.uniform(2, 4)

    def move(self, mouse_x, mouse_y):
        # Drift particle
        self.x += self.vx
        self.y += self.vy

        # Bounce off canvas edges
        if self.x <= 0 or self.x >= self.width:
            self.vx *= -1
        if self.y <= 0 or self.y >= self.height:
            self.vy *= -1

        # Mouse interaction: Slight attraction pull toward cursor
        if mouse_x is not None and mouse_y is not None:
            dx = mouse_x - self.x
            dy = mouse_y - self.y
            dist = math.hypot(dx, dy)
            if dist < 120 and dist > 0:
                self.x += (dx / dist) * 0.8
                self.y += (dy / dist) * 0.8


class ConstellationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Particle Constellation")
        self.width = 800
        self.height = 600
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(bg="#0b0f19")
        self.root.resizable(False, False)

        # Canvas Setup
        self.canvas = tk.Canvas(
            root, width=self.width, height=self.height, 
            bg="#0b0f19", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Track Mouse Coordinates
        self.mouse_x = None
        self.mouse_y = None
        self.canvas.bind("<Motion>", self.track_mouse)
        self.canvas.bind("<Leave>", self.clear_mouse)

        # Create Particles
        self.num_particles = 70
        self.particles = [Particle(self.width, self.height) for _ in range(self.num_particles)]

        # Start Render Loop
        self.animate()

    def track_mouse(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def clear_mouse(self, event):
        self.mouse_x = None
        self.mouse_y = None

    def animate(self):
        self.canvas.delete("all")

        # Update and render particles
        for i, p1 in enumerate(self.particles):
            p1.move(self.mouse_x, self.mouse_y)

            # Draw connections between nearby particles
            for p2 in self.particles[i + 1:]:
                dist = math.hypot(p1.x - p2.x, p1.y - p2.y)
                if dist < 110:
                    # Fade line intensity based on distance
                    opacity_factor = int(255 * (1 - (dist / 110)))
                    color = f"#{opacity_factor:02x}a8ff"
                    self.canvas.create_line(
                        p1.x, p1.y, p2.x, p2.y, 
                        fill="#38bdf8", width=1
                    )

            # Draw particle node
            self.canvas.create_oval(
                p1.x - p1.radius, p1.y - p1.radius,
                p1.x + p1.radius, p1.y + p1.radius,
                fill="#00f0ff", outline=""
            )

        # 60 FPS animation cycle (~16 milliseconds)
        self.root.after(16, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = ConstellationApp(root)
    root.mainloop()