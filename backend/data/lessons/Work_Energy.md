## Introduction

Energy surrounds us in countless forms—from the chemical energy in our food to the electrical energy powering our devices, from the gravitational potential energy of a boulder perched on a cliff to the kinetic energy of a sprinter crossing the finish line. Understanding energy and the concept of work provides us with powerful tools to analyze and predict the behavior of physical systems without having to track complex force interactions at every moment.

In this lesson, we'll explore the fundamental concepts of work and energy, their mathematical representations, and the principle of energy conservation. We'll see how these concepts simplify the analysis of many physical problems and connect to real-world applications.

## Key Concepts and Principles

### Work

Work is the transfer of energy that occurs when a force moves an object through a distance. Mathematically, work is defined as the dot product of the force vector and the displacement vector:

$$W = \vec{F} \cdot \vec{d} = F \, d \, \cos\theta$$

Where:
- $W$ is the work done (joules, J)
- $\vec{F}$ is the force vector (newtons, N)
- $\vec{d}$ is the displacement vector (meters, m)
- $\theta$ is the angle between the force and displacement vectors

Key insights about work:
- Work is a scalar quantity (not a vector)
- Work can be positive, negative, or zero
- Work is path-independent only for conservative forces

### Energy

Energy is the capacity to do work. It exists in many forms, but for mechanical systems, we focus primarily on:

1. **Kinetic Energy (K)**: Energy of motion, given by:
   $$K = \frac{1}{2}mv^2$$
   Where $m$ is mass and $v$ is speed.

2. **Potential Energy (U)**: Energy due to position or configuration:
   - **Gravitational potential energy** near Earth's surface:
     $$U_g = mgh$$
     Where $m$ is mass, $g$ is gravitational acceleration, and $h$ is height.
   - **Elastic potential energy** in a spring:
     $$U_e = \frac{1}{2}kx^2$$
     Where $k$ is the spring constant and $x$ is the displacement from equilibrium.

### Work-Energy Theorem

The Work-Energy Theorem states that the net work done on an object equals the change in its kinetic energy:

$$W_{\text{net}} = \Delta K = K_f - K_i = \frac{1}{2}mv_f^2 - \frac{1}{2}mv_i^2$$

This theorem provides a powerful alternative to using Newton's Second Law directly, especially when we're more interested in the beginning and end states than in the details of motion.

### Conservative Forces

A force is conservative if the work it does on an object moving between two points is independent of the path taken. For conservative forces:
- Work depends only on the initial and final positions
- Work done around any closed path is zero
- We can define a potential energy function

Examples include gravitational force, elastic spring force, and electrostatic force.

### Conservation of Mechanical Energy

When only conservative forces do work on a system, the total mechanical energy (kinetic plus potential) remains constant:

$$E = K + U = \text{constant}$$
$$K_i + U_i = K_f + U_f$$

This principle allows us to relate the energy at different positions without needing to calculate the work explicitly.

### Non-Conservative Forces and Energy

Non-conservative forces (like friction) don't have an associated potential energy function. When they act:

$$\Delta E = W_{\text{nc}}$$

Where $W_{\text{nc}}$ is the work done by non-conservative forces.

For friction, this work is typically negative, reducing the total mechanical energy of the system.

## Important Formulas

1. **Work**:
   $$W = \vec{F} \cdot \vec{d} = F \, d \, \cos\theta$$

2. **Kinetic Energy**:
   $$K = \frac{1}{2}mv^2$$

3. **Gravitational Potential Energy** (near Earth's surface):
   $$U_g = mgh$$

4. **Elastic Potential Energy**:
   $$U_e = \frac{1}{2}kx^2$$

5. **Work-Energy Theorem**:
   $$W_{\text{net}} = \Delta K$$

6. **Conservation of Mechanical Energy**:
   $$K_i + U_i = K_f + U_f$$

7. **Power** (rate of doing work):
   $$P = \frac{dW}{dt} = \vec{F} \cdot \vec{v}$$

## Real-World Applications

1. **Roller Coasters**:
   Roller coasters demonstrate energy transformations between gravitational potential and kinetic energy. The initial climb converts work done by motors into potential energy, which then transforms into kinetic energy during descent, with some losses due to friction.

2. **Hydroelectric Power**:
   Dams convert the gravitational potential energy of water into electrical energy. Water at height has potential energy that converts to kinetic energy as it falls, turning turbines to generate electricity.

3. **Vehicle Braking Systems**:
   When a car brakes, friction converts kinetic energy into thermal energy. In regenerative braking systems used in electric vehicles, some of this energy is captured and stored in batteries.

4. **Sports and Athletics**:
   In pole vaulting, athletes convert kinetic energy from their run into elastic potential energy in the bending pole, which then helps convert this energy into gravitational potential energy as they clear the bar.

5. **Pendulum Clocks**:
   Pendulum clocks operate on the principle of energy conservation, with energy continuously converting between kinetic and potential forms as the pendulum swings.

## Example Problems with Solutions

### Example 1: Work Done Against Gravity

**Problem:** A 70 kg hiker climbs a mountain trail, gaining 500 meters in elevation. How much work is done by the hiker against gravity?

**Solution:**

Given:
- Mass of hiker ($m$) = 70 kg
- Change in elevation ($h$) = 500 m
- Gravitational acceleration ($g$) = 9.8 m/s²

The work done against gravity equals the change in gravitational potential energy:

$$W = mgh = 70 \, \text{kg} \times 9.8 \, \text{m/s}^2 \times 500 \, \text{m} = 343,000 \, \text{J} = 343 \, \text{kJ}$$

The hiker does 343 kJ of work against gravity.

### Example 2: Work-Energy Theorem

**Problem:** A 1500 kg car accelerates from rest to 25 m/s. Calculate:
a) The change in kinetic energy
b) The net work done on the car

**Solution:**

Given:
- Mass of car ($m$) = 1500 kg
- Initial velocity ($v_i$) = 0 m/s
- Final velocity ($v_f$) = 25 m/s

a) The change in kinetic energy is:

$$\Delta K = K_f - K_i = \frac{1}{2}mv_f^2 - \frac{1}{2}mv_i^2 = \frac{1}{2}m(v_f^2 - v_i^2)$$

$$\Delta K = \frac{1}{2} \times 1500 \, \text{kg} \times (25^2 - 0^2) \, \text{m}^2/\text{s}^2 = 750 \times 625 = 468,750 \, \text{J} = 469 \, \text{kJ}$$

b) According to the Work-Energy Theorem, the net work equals the change in kinetic energy:

$$W_{\text{net}} = \Delta K = 469 \, \text{kJ}$$

The net work done on the car is 469 kJ.

### Example 3: Conservation of Energy with a Spring

**Problem:** A 2 kg block is pressed against a spring with spring constant $k = 500 \, \text{N/m}$, compressing it by 20 cm. If the block is released on a frictionless horizontal surface, what will be its speed after it loses contact with the spring?

**Solution:**

Given:
- Mass of block ($m$) = 2 kg
- Spring constant ($k$) = 500 N/m
- Initial compression ($x$) = 0.20 m

Initially, the block has elastic potential energy and no kinetic energy. After release, the elastic potential energy is converted to kinetic energy.

Initial state:
- Kinetic energy: $K_i = 0$
- Potential energy: $U_i = \frac{1}{2}kx^2 = \frac{1}{2} \times 500 \, \text{N/m} \times (0.20 \, \text{m})^2 = 10 \, \text{J}$

Final state (after losing contact with the spring):
- Kinetic energy: $K_f = \frac{1}{2}mv^2$
- Potential energy: $U_f = 0$ (spring no longer compressed)

By conservation of energy:

$$K_i + U_i = K_f + U_f$$
$$0 + 10 \, \text{J} = \frac{1}{2} \times 2 \, \text{kg} \times v^2 + 0$$

Solving for $v$:

$$v = \sqrt{\frac{2 \times 10 \, \text{J}}{2 \, \text{kg}}} = \sqrt{10} \approx 3.16 \, \text{m/s}$$

The block's speed will be approximately 3.16 m/s after losing contact with the spring.

### Example 4: Energy with Non-Conservative Forces

**Problem:** A 50 kg crate slides down a 30° incline with a coefficient of kinetic friction $\mu_k = 0.25$. If the crate starts from rest and the incline is 10 meters long, what is the crate's speed at the bottom?

**Solution:**

Given:
- Mass of crate ($m$) = 50 kg
- Angle of incline ($\theta$) = 30°
- Coefficient of kinetic friction ($\mu_k$) = 0.25
- Length of incline ($L$) = 10 m
- Initial velocity ($v_i$) = 0 m/s

First, calculate the change in height:

$$h = L \sin\theta = 10 \, \text{m} \times \sin(30°) = 10 \, \text{m} \times 0.5 = 5 \, \text{m}$$

The change in gravitational potential energy is:

$$\Delta U_g = -mgh = -50 \, \text{kg} \times 9.8 \, \text{m/s}^2 \times 5 \, \text{m} = -2450 \, \text{J}$$

The work done by friction is:

$$W_{\text{friction}} = -f \times L = -\mu_k mg\cos\theta \times L$$
$$W_{\text{friction}} = -0.25 \times 50 \, \text{kg} \times 9.8 \, \text{m/s}^2 \times \cos(30°) \times 10 \, \text{m}$$
$$W_{\text{friction}} = -0.25 \times 50 \times 9.8 \times 0.866 \times 10 = -1060 \, \text{J}$$

The change in kinetic energy equals the negative change in potential energy plus the work done by friction:

$$\Delta K = -\Delta U_g + W_{\text{friction}} = 2450 \, \text{J} - 1060 \, \text{J} = 1390 \, \text{J}$$

Since $K_i = 0$ (starts from rest), we have $K_f = 1390 \, \text{J}$.

Using $K_f = \frac{1}{2}mv_f^2$, we can find the final velocity:

$$v_f = \sqrt{\frac{2K_f}{m}} = \sqrt{\frac{2 \times 1390 \, \text{J}}{50 \, \text{kg}}} = \sqrt{55.6} \approx 7.46 \, \text{m/s}$$

The crate's speed at the bottom of the incline is approximately 7.46 m/s.

By understanding work and energy principles, we gain powerful tools for analyzing physical systems without having to track forces at every moment. These concepts form the foundation for more advanced topics in physics and engineering, from thermodynamics to quantum mechanics.