## Introduction

Rotational dynamics is the branch of physics that studies the motion of objects rotating about an axis and the forces that cause or affect such motion. Just as linear dynamics deals with objects in straight-line motion, rotational dynamics focuses on objects spinning or rotating, such as wheels, gears, planets, and even galaxies. Understanding rotational dynamics allows us to analyze and predict how objects behave when subjected to torque, friction, and other rotational effects.

In this lesson, we will explore the fundamental principles governing rotational motion, understand essential quantities like angular velocity, angular acceleration, torque, and moment of inertia, and apply these concepts to solve practical problems.

## Key Concepts and Principles

### Rotational Motion vs. Translational Motion
In linear (translational) motion, we are concerned with linear displacement, velocity, acceleration, force, and mass. Rotational motion has analogous quantities:

- **Angular displacement ($\theta$)**: The angle through which an object rotates, measured in radians (rad).
- **Angular velocity ($\omega$)**: The rate at which angular displacement changes, measured in radians per second (rad/s).
- **Angular acceleration ($\alpha$)**: The rate at which angular velocity changes, measured in radians per second squared (rad/s²).
- **Torque ($\tau$)**: A rotational equivalent of force that causes or changes rotational motion, measured in Newton-meters (N m).
- **Moment of inertia ($I$)**: A measure of an object's resistance to rotational acceleration, analogous to mass in linear motion, measured in kilogram-meter squared (kg m²).

### Torque and Rotational Equilibrium
Torque ($\tau$) depends on the applied force ($F$), the distance from the axis of rotation to the point where the force is applied ($r$), and the angle ($\phi$) between the force and the lever arm:

$$
\tau = rF\sin\phi
$$

Torque creates angular acceleration ($\alpha$) in proportion to the moment of inertia ($I$):

$$
\tau = I\alpha
$$

### Moment of Inertia 
The moment of inertia ($I$) depends on the distribution of mass around the axis of rotation. For discrete masses, it is calculated as:

$$
I = \sum m_i r_i^2
$$

For continuous objects, integrals are used to sum the contributions of infinitesimal mass elements:

$$
I = \int r^2\,dm
$$

Different shapes have well-known moments of inertia. For example:

- Solid cylinder or disk about central axis: $I = \frac{1}{2}MR^2$
- Solid sphere about a diameter: $I = \frac{2}{5}MR^2$
- Thin hoop about central axis: $I = MR^2$

### Rotational Kinetic Energy
An object in rotational motion possesses rotational kinetic energy ($K_{rot}$):

$$
K_{rot} = \frac{1}{2}I\omega^2
$$

This is analogous to the translational kinetic energy formula ($\frac{1}{2}mv^2$).

### Angular Momentum
Angular momentum ($L$) is a measure of rotational inertia in motion, given by:

$$
L = I\omega
$$

Angular momentum is conserved in isolated systems (no external torque), analogous to linear momentum conservation.


## Important Formulas

1. **Angular displacement, velocity, acceleration relations:**

$$
\omega = \frac{\Delta \theta}{\Delta t}, \quad \alpha = \frac{\Delta \omega}{\Delta t}
$$

2. **Torque definition:**

$$
\tau = rF\sin\phi
$$

3. **Newton's second law for rotation:**

$$
\tau = I\alpha
$$

4. **Moment of inertia (discrete and continuous):**

Discrete: 
$$
I = \sum m_i r_i^2
$$

Continuous: 
$$
I = \int r^2\,dm
$$

5. **Rotational kinetic energy:**

$$
K_{rot} = \frac{1}{2}I\omega^2
$$

6. **Angular momentum:**

$$
L = I\omega
$$

7. **Conservation of angular momentum (no external torque):**

$$
I_i\omega_i = I_f\omega_f
$$



## Real-world Applications

### 1. Gymnastics and Diving
Athletes performing spins, flips, and rotations utilize conservation of angular momentum. By pulling their arms or legs closer to the body, they reduce their moment of inertia and thus spin faster, allowing for precise control of their rotation speed.

### 2. Wheels and Gears in Machinery
Rotational dynamics principles allow engineers to design efficient machines. Understanding torque and moment of inertia is crucial in choosing the right motor or gear system for automobiles, bicycles, and industrial equipment.

### 3. Satellite and Spacecraft Orientation
Satellites and spacecraft use rotating wheels (reaction wheels) or thrusters to control orientation. Precise calculations of angular momentum and torque enable accurate adjustments to spacecraft orientation in space.

### 4. Rotating Doors and Flywheels
Revolving doors and flywheels in engines rely on rotational motion principles. A flywheel stores rotational kinetic energy and smooths out fluctuations in energy delivery within machines.



## Example Problems with Solutions

### Example 1: Calculating Torque
A force of 20 N is applied perpendicularly to the end of a wrench that is 0.3 m long. What is the magnitude of the torque?

**Solution:**
Given:
- Force, $F = 20\,\text{N}$
- Lever arm length, $r = 0.3\,\text{m}$
- Angle, $\phi = 90^\circ$, thus $\sin(90^\circ) = 1$

Then,

$$
\tau = rF\sin\phi = (0.3\,\text{m})(20\,\text{N})(1) = 6\,\text{N m}
$$

Therefore, the torque magnitude is $6\,\text{N m}$.

### Example 2: Angular Acceleration of a Disk
A solid disk with mass 5 kg and radius 0.2 m experiences a net torque of 2 N m. Calculate its angular acceleration.

**Solution:**
Given:
- Mass, $M = 5\,\text{kg}$
- Radius, $R = 0.2\,\text{m}$
- Torque, $\tau = 2\,\text{N m}$

Moment of inertia for a solid disk about its central axis:

$$
I = \frac{1}{2}MR^2 = \frac{1}{2}(5\,\text{kg})(0.2\,\text{m})^2 = 0.1\,\text{kg m}^2
$$

Using $\tau = I\alpha$, we solve for angular acceleration $\alpha$:

$$
\alpha = \frac{\tau}{I} = \frac{2\,\text{N m}}{0.1\,\text{kg m}^2} = 20\,\text{rad/s}^2
$$

Thus, the angular acceleration is $20\,\text{rad/s}^2$.

### Example 3: Conservation of Angular Momentum
An ice skater spinning with arms extended has a moment of inertia of 4 kg m² and angular velocity of 3 rad/s. She pulls her arms in, reducing her moment of inertia to 2 kg m². Determine her new angular velocity.

**Solution:**
Given:
- Initial moment of inertia, $I_i = 4\,\text{kg m}^2$
- Initial angular velocity, $\omega_i = 3\,\text{rad/s}$
- Final moment of inertia, $I_f = 2\,\text{kg m}^2$

Using conservation of angular momentum ($I_i\omega_i = I_f\omega_f$), we find the final angular velocity:

$$
\omega_f = \frac{I_i\omega_i}{I_f} = \frac{(4\,\text{kg m}^2)(3\,\text{rad/s})}{2\,\text{kg m}^2} = 6\,\text{rad/s}
$$

Thus, her new angular velocity is $6\,\text{rad/s}$, doubling her original rotation rate.