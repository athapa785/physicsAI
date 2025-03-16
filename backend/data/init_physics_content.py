"""
Initialize sample physics content for the RAG system.
This script creates text files with physics content from University Physics.
"""

import os
import json

# Physics content organized by major categories from University Physics
PHYSICS_CONTENT = {
    "mechanics": {
        "kinematics_1d": """
# One-Dimensional Kinematics

## Key Concepts
- Position, displacement, velocity, and acceleration
- Motion with constant velocity
- Motion with constant acceleration
- Free fall motion

## Mathematical Formulas
For motion with constant acceleration:
- Velocity: \(v(t) = v_0 + at\)
- Position: \(x(t) = x_0 + v_0t + \frac{1}{2}at^2\)
- Velocity-position relation: \(v^2 = v_0^2 + 2a(x - x_0)\)

## Examples
1. Free Fall Motion
A ball is dropped from a height of 20m. Find:
a) Time to reach ground
b) Final velocity before impact

Solution:
Using \(y(t) = y_0 + v_0t - \frac{1}{2}gt^2\):
- Initial conditions: \(y_0 = 20\text{ m}\), \(v_0 = 0\), \(g = 9.81\text{ m/s}^2\)
- At ground: \(y = 0\)
- Time: \(t = \sqrt{\frac{2y_0}{g}} = \sqrt{\frac{2(20)}{9.81}} = 2.02\text{ s}\)
- Final velocity: \(v = gt = 9.81(2.02) = 19.82\text{ m/s}\) downward
""",
        "forces_newtons_laws": """
# Newton's Laws of Motion

## Key Concepts
- First Law: An object remains at rest or in uniform motion unless acted upon by a net force
- Second Law: \(\vec{F} = m\vec{a}\)
- Third Law: For every action, there is an equal and opposite reaction

## Applications
1. Weight and Normal Force
- Weight: \(\vec{W} = m\vec{g}\)
- Normal force balances weight on horizontal surfaces

2. Tension and Friction
- Tension in ropes and strings
- Static friction: \(f_s \leq \mu_s N\)
- Kinetic friction: \(f_k = \mu_k N\)

## Example
A 2kg block is pulled across a rough surface (μₖ = 0.3) by a 10N force at 30° above horizontal.
Find:
a) Normal force
b) Friction force
c) Acceleration

Solution:
1. Forces in y-direction:
   \(N + F\sin(30°) - mg = 0\)
   \(N = 19.6 - 5 = 14.6\text{ N}\)

2. Friction force:
   \(f_k = \mu_k N = 0.3(14.6) = 4.38\text{ N}\)

3. Net force in x-direction:
   \(F_{\text{net}} = F\cos(30°) - f_k = 8.66 - 4.38 = 4.28\text{ N}\)
   \(a = \frac{F_{\text{net}}}{m} = \frac{4.28}{2} = 2.14\text{ m/s}^2\)
""",
    },
    "thermodynamics": {
        "heat_and_temperature": """
# Heat and Temperature

## Key Concepts
- Temperature scales (Celsius, Kelvin, Fahrenheit)
- Heat as energy transfer
- Specific heat capacity
- Phase changes and latent heat
- Heat transfer methods: conduction, convection, radiation

## Mathematical Formulas
- Temperature conversion: \(T_K = T_C + 273.15\)
- Heat energy: \(Q = mc\Delta T\)
- Latent heat: \(Q = mL\)
- Heat conduction: \(P = \frac{kA\Delta T}{d}\)
- Stefan-Boltzmann law: \(P = \sigma AT^4\)

## Example
A 100g block of ice at 0°C is converted to water at 20°C.
Find the total heat energy required given:
- Latent heat of fusion of ice = 334 kJ/kg
- Specific heat capacity of water = 4186 J/kg·K

Solution:
1. Heat to melt ice:
   \(Q_1 = mL = 0.1\text{ kg} \times 334000\text{ J/kg} = 33400\text{ J}\)

2. Heat to warm water:
   \(Q_2 = mc\Delta T = 0.1\text{ kg} \times 4186\text{ J/kg·K} \times 20\text{ K} = 8372\text{ J}\)

3. Total heat:
   \(Q_{total} = Q_1 + Q_2 = 41772\text{ J}\)
""",
    },
    "electromagnetism": {
        "electric_fields": """
# Electric Fields and Forces

## Key Concepts
- Electric charge and Coulomb's law
- Electric field lines and field strength
- Electric potential and potential difference
- Conductors and insulators
- Gauss's law

## Mathematical Formulas
- Coulomb's law: \(F = k\frac{q_1q_2}{r^2}\)
- Electric field: \(E = \frac{F}{q} = k\frac{Q}{r^2}\)
- Electric potential: \(V = k\frac{Q}{r}\)
- Electric potential energy: \(U = k\frac{q_1q_2}{r}\)
- Gauss's law: \(\oint \vec{E} \cdot d\vec{A} = \frac{Q_{enc}}{\epsilon_0}\)

## Example
Two point charges, q₁ = 2μC and q₂ = -3μC, are separated by 0.1m.
Calculate:
a) The electric force between them
b) The electric field at the midpoint

Solution:
1. Electric force:
   \(F = k\frac{q_1q_2}{r^2}\)
   \(F = (9 \times 10^9)\frac{(2 \times 10^{-6})(-3 \times 10^{-6})}{(0.1)^2}\)
   \(F = -5.4\text{ N}\) (attractive force)

2. Electric field at midpoint:
   From q₁: \(E_1 = k\frac{q_1}{(0.05)^2} = 7.2 \times 10^6\text{ N/C}\)
   From q₂: \(E_2 = k\frac{q_2}{(0.05)^2} = -10.8 \times 10^6\text{ N/C}\)
   Net field: \(E_{net} = -3.6 \times 10^6\text{ N/C}\) (toward q₂)
""",
    },
    "waves_oscillations": {
        "simple_harmonic_motion": """
# Simple Harmonic Motion

## Key Concepts
- Periodic motion with restoring force proportional to displacement
- Examples: mass on spring, simple pendulum
- Angular frequency: \(\omega = \sqrt{\frac{k}{m}}\) for mass-spring system
- Period: \(T = 2\pi\sqrt{\frac{m}{k}}\)

## Mathematical Description
1. Position: \(x(t) = A\cos(\omega t + \phi)\)
2. Velocity: \(v(t) = -A\omega\sin(\omega t + \phi)\)
3. Acceleration: \(a(t) = -A\omega^2\cos(\omega t + \phi)\)

## Energy in SHM
- Kinetic Energy: \(K = \frac{1}{2}mv^2\)
- Potential Energy: \(U = \frac{1}{2}kx^2\)
- Total Energy: \(E = \frac{1}{2}kA^2\)

## Example
A 0.5kg mass on a spring with k = 20 N/m is displaced 0.1m and released.
Find:
a) Angular frequency
b) Period
c) Maximum velocity

Solution:
1. \(\omega = \sqrt{\frac{k}{m}} = \sqrt{\frac{20}{0.5}} = 6.32\text{ rad/s}\)
2. \(T = \frac{2\pi}{\omega} = 0.99\text{ s}\)
3. \(v_{\text{max}} = A\omega = 0.1(6.32) = 0.632\text{ m/s}\)
""",
    }
}

def create_physics_content():
    """Create physics content files in the data directory."""
    content_dir = os.path.join(os.path.dirname(__file__), "physics_content")
    os.makedirs(content_dir, exist_ok=True)
    
    # Create content files
    for category, topics in PHYSICS_CONTENT.items():
        category_dir = os.path.join(content_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        for topic_name, content in topics.items():
            file_path = os.path.join(category_dir, f"{topic_name}.txt")
            with open(file_path, "w") as f:
                f.write(content.strip())
            print(f"Created {file_path}")

if __name__ == "__main__":
    create_physics_content()
