Fragmentum: Physics-Based Ball Fragmentation Simulator

This project started as an inspiration from my high school days. What if I could simulate chain fragmentation using the all the mechanics concepts and logic I have practiced for so long for the Joint Entrance Examination (JEE)? A few hundred lines later, I ended up with Fragmentum, a canvas-based simulation where bouncing balls split into generational fragments based on their velocity, size, and collision dynamics.

Each ball reacts to forces like gravity, air resistance, and canvas boundaries, and if it’s moving fast enough (and isn’t too small or old), it splits into smaller fragments which then continue the simulation on their own. There's no restart button. The simulation ends, when all balls die out.

🎯 Features
Canvas simulation using graphics.py.
Here, each ball has:

  Independent velocity and mass.

  Basic physics-based motion and bounce logic.

  A recursive splitting behavior based on speed and generation.

  Visual color coding for ball generations.

  Simple end condition: the simulation stops when no balls remain.

🧠 What I Learned
This was one of the first times I went from raw physics equations to something visually alive. I got a deeper grip on:

  Vector math, trigonometry, and motion simulation.

  Writing clean, modular OOP code for animations.

  Building logic that can evolve without needing constant input.

🛠️ Tech Stack
    Language: Python
    Graphics: graphics.py
    Modules Used: math, random, time

📸 A Preview!
<p align="center">
  <img src="preview.gif" alt="A look at the simulation!" width="500"/>
</p>

This project was originally built as part of Stanford's Code in Place 2025 program (Experienced Track), and was written for Stanford's browser-based IDE with access to the `Canvas` module. While the code is open for reference, **it won’t run locally as-is** unless the environment has the custom `graphics.Canvas` class that was used in the course setup.