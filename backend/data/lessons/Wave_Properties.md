## Introduction

Waves are ubiquitous in nature and play a fundamental role in numerous physical phenomena. From the ripples on a pond to the electromagnetic waves that carry information across the globe, wave behavior underlies many of the most important processes in our universe. Understanding wave properties is essential for fields ranging from acoustics and optics to quantum mechanics and telecommunications.

At its most basic level, a wave is a disturbance that transfers energy through a medium or space without causing any permanent displacement of the medium itself. This simple definition encompasses an incredible variety of phenomena, from mechanical waves like sound and water waves to electromagnetic waves like light and radio waves, and even to the probability waves of quantum mechanics.

What makes waves particularly fascinating is that despite their diverse manifestations, they share common properties and behaviors that can be described by a unified mathematical framework. These common properties include amplitude, wavelength, frequency, period, wave speed, and phase. Waves also exhibit characteristic behaviors such as reflection, refraction, diffraction, interference, and the Doppler effect.

In this lesson, we will explore these fundamental properties and behaviors of waves, providing a solid foundation for understanding more complex wave phenomena in various branches of physics.

## Key Concepts and Principles

### Types of Waves

Waves can be classified in several ways:

1. **Based on Medium Requirements**:
   - **Mechanical Waves**: Require a medium to propagate (e.g., sound waves, water waves, seismic waves)
   - **Electromagnetic Waves**: Do not require a medium and can travel through vacuum (e.g., light, radio waves, X-rays)
   - **Matter Waves**: Associated with particles with mass (described by quantum mechanics)

2. **Based on Direction of Oscillation**:
   - **Transverse Waves**: Particles of the medium oscillate perpendicular to the direction of wave propagation (e.g., electromagnetic waves, waves on a string)
   - **Longitudinal Waves**: Particles of the medium oscillate parallel to the direction of wave propagation (e.g., sound waves, compression waves)
   - **Surface Waves**: Particles move in both transverse and longitudinal directions (e.g., water waves)

3. **Based on Dimensionality**:
   - **One-dimensional Waves**: Propagate along a line (e.g., waves on a string)
   - **Two-dimensional Waves**: Propagate over a surface (e.g., ripples on water)
   - **Three-dimensional Waves**: Propagate through a volume (e.g., sound waves in air)

4. **Based on Shape**:
   - **Traveling Waves**: Move from one location to another
   - **Standing Waves**: Appear to stay in place, resulting from the superposition of two identical waves traveling in opposite directions

### Fundamental Wave Parameters

1. **Amplitude (A)**: The maximum displacement of a particle from its equilibrium position. It is related to the energy carried by the wave—the larger the amplitude, the greater the energy.

2. **Wavelength (λ)**: The distance between two consecutive points in phase (e.g., from crest to crest or trough to trough). Measured in meters (m).

3. **Frequency (f)**: The number of complete oscillations per unit time. Measured in hertz (Hz), where 1 Hz = 1 cycle per second.

4. **Period (T)**: The time taken for one complete oscillation. Measured in seconds (s). Related to frequency by $T = \frac{1}{f}$.

5. **Wave Speed (v)**: The speed at which the wave propagates through the medium. Related to wavelength and frequency by $v = \lambda f$. Measured in meters per second (m/s).

6. **Angular Frequency (ω)**: The rate of change of the phase angle, given by $\omega = 2\pi f$. Measured in radians per second (rad/s).

7. **Wavenumber (k)**: The spatial frequency of the wave, given by $k = \frac{2\pi}{\lambda}$. Measured in radians per meter (rad/m).

8. **Phase (φ)**: Describes the position of a point within a wave cycle, usually expressed as an angle in radians.

### Wave Equation

The one-dimensional wave equation, which describes the propagation of waves, is:

$$\frac{\partial^2 y}{\partial t^2} = v^2 \frac{\partial^2 y}{\partial x^2}$$

Where:
- $y$ is the displacement
- $t$ is time
- $x$ is position
- $v$ is the wave speed

A general solution to this equation for a traveling wave is:

$$y(x, t) = A \sin(kx - \omega t + \phi)$$

Or equivalently:

$$y(x, t) = A \sin\left(2\pi\left(\frac{x}{\lambda} - \frac{t}{T}\right) + \phi\right)$$

Where $A$ is the amplitude, $k$ is the wavenumber, $\omega$ is the angular frequency, and $\phi$ is the phase constant.

### Wave Behaviors

1. **Reflection**: The bouncing back of a wave when it encounters a boundary. The angle of incidence equals the angle of reflection.

2. **Refraction**: The bending of a wave as it passes from one medium to another due to a change in wave speed. Described by Snell's Law:
   $$\frac{\sin \theta_1}{\sin \theta_2} = \frac{v_1}{v_2} = \frac{n_2}{n_1}$$
   Where $\theta_1$ and $\theta_2$ are the angles of incidence and refraction, $v_1$ and $v_2$ are the wave speeds in the respective media, and $n_1$ and $n_2$ are the refractive indices.

3. **Diffraction**: The bending of waves around obstacles or through apertures. More pronounced when the size of the obstacle or aperture is comparable to the wavelength.

4. **Interference**: The superposition of two or more waves to form a resultant wave. Can be:
   - **Constructive Interference**: Waves reinforce each other, resulting in a larger amplitude
   - **Destructive Interference**: Waves cancel each other, resulting in a smaller amplitude

5. **Doppler Effect**: The change in observed frequency due to relative motion between the source and observer. For waves in a medium:
   - When the observer moves toward the source: $f' = f\left(\frac{v + v_o}{v}\right)$
   - When the observer moves away from the source: $f' = f\left(\frac{v - v_o}{v}\right)$
   - When the source moves toward the observer: $f' = f\left(\frac{v}{v - v_s}\right)$
   - When the source moves away from the observer: $f' = f\left(\frac{v}{v + v_s}\right)$
   
   Where $f'$ is the observed frequency, $f$ is the emitted frequency, $v$ is the wave speed in the medium, $v_o$ is the observer's speed, and $v_s$ is the source's speed.

### Standing Waves

Standing waves result from the superposition of two identical waves traveling in opposite directions. They are characterized by:

1. **Nodes**: Points that remain stationary (zero amplitude)
2. **Antinodes**: Points that oscillate with maximum amplitude

The equation for a standing wave is:

$$y(x, t) = 2A \sin(kx) \cos(\omega t)$$

Standing waves in a string fixed at both ends (e.g., a guitar string) have wavelengths given by:

$$\lambda_n = \frac{2L}{n}$$

Where $L$ is the length of the string and $n = 1, 2, 3, ...$ is the harmonic number.

The corresponding frequencies are:

$$f_n = \frac{v}{\lambda_n} = \frac{nv}{2L}$$

Where $v$ is the wave speed in the string.

### Wave Intensity and Energy

The intensity of a wave is the power transmitted per unit area, measured in watts per square meter (W/m²):

$$I = \frac{P}{A}$$

For a spherical wave spreading out in three dimensions, the intensity decreases with the square of the distance from the source:

$$I \propto \frac{1}{r^2}$$

The energy carried by a wave is proportional to the square of its amplitude:

$$E \propto A^2$$

### Wave Speed in Different Media

1. **Waves on a String**:
   $$v = \sqrt{\frac{T}{\mu}}$$
   Where $T$ is the tension in the string and $\mu$ is the linear mass density.

2. **Sound Waves in a Fluid**:
   $$v = \sqrt{\frac{B}{\rho}}$$
   Where $B$ is the bulk modulus and $\rho$ is the density of the fluid.

3. **Sound Waves in a Solid Rod**:
   $$v = \sqrt{\frac{Y}{\rho}}$$
   Where $Y$ is Young's modulus and $\rho$ is the density of the solid.

4. **Electromagnetic Waves in Vacuum**:
   $$v = c = \frac{1}{\sqrt{\epsilon_0 \mu_0}}$$
   Where $c$ is the speed of light, $\epsilon_0$ is the permittivity of free space, and $\mu_0$ is the permeability of free space.

## Important Formulas

1. **Wave Speed**:
   $$v = \lambda f = \frac{\omega}{k}$$

2. **Period and Frequency**:
   $$T = \frac{1}{f}$$

3. **Angular Frequency**:
   $$\omega = 2\pi f$$

4. **Wavenumber**:
   $$k = \frac{2\pi}{\lambda}$$

5. **Traveling Wave Equation**:
   $$y(x, t) = A \sin(kx - \omega t + \phi)$$

6. **Standing Wave Equation**:
   $$y(x, t) = 2A \sin(kx) \cos(\omega t)$$

7. **Snell's Law**:
   $$n_1 \sin \theta_1 = n_2 \sin \theta_2$$

8. **Doppler Effect (General Form)**:
   $$f' = f\left(\frac{v \pm v_o}{v \mp v_s}\right)$$

9. **Intensity of a Wave**:
   $$I = \frac{1}{2}\rho \omega^2 A^2 v$$
   Where $\rho$ is the density of the medium.

10. **Resonant Frequencies for a String Fixed at Both Ends**:
    $$f_n = \frac{n}{2L}\sqrt{\frac{T}{\mu}}$$
    Where $n = 1, 2, 3, ...$

## Real-World Applications

1. **Acoustics and Music**:
   - Musical instruments produce sound through standing waves in strings, air columns, or membranes
   - Concert hall design uses principles of reflection and absorption to optimize sound quality
   - Ultrasound imaging in medicine uses high-frequency sound waves to create images of internal body structures

2. **Optics and Electromagnetic Waves**:
   - Fiber optic communication systems use total internal reflection to transmit information via light waves
   - Diffraction gratings separate light into its component wavelengths in spectrometers
   - Interference is used in anti-reflective coatings for camera lenses and eyeglasses
   - Radio and television broadcasting rely on electromagnetic wave transmission

3. **Seismology**:
   - Seismic waves (P-waves and S-waves) provide information about Earth's interior structure
   - Earthquake detection and analysis use principles of wave propagation

4. **Medical Imaging and Therapy**:
   - MRI (Magnetic Resonance Imaging) uses radio waves and magnetic fields to create detailed images of the body
   - Radiation therapy for cancer treatment uses high-energy electromagnetic waves
   - Lithotripsy uses shock waves to break up kidney stones

5. **Telecommunications**:
   - Mobile phones use electromagnetic waves to transmit voice and data
   - Satellite communication systems rely on microwave transmission
   - Radar systems use reflection of radio waves to detect objects

6. **Quantum Mechanics**:
   - Matter waves describe the wave-like behavior of particles
   - The wave function in quantum mechanics gives the probability amplitude for finding a particle in a particular state

7. **Engineering**:
   - Vibration analysis in structural engineering uses principles of wave mechanics
   - Noise cancellation technology uses destructive interference to reduce unwanted sound
   - Sonar systems use sound wave reflection to map underwater terrain

## Example Problems with Solutions

### Example 1: Wave Speed, Frequency, and Wavelength

**Problem:** A wave traveling along a string has a wavelength of 0.5 meters and a frequency of 20 Hz. Calculate:
a) The wave speed
b) The period of the wave
c) The angular frequency
d) The wavenumber

**Solution:**

Given:
- Wavelength ($\lambda$) = 0.5 m
- Frequency ($f$) = 20 Hz

a) The wave speed is:
$$v = \lambda f = 0.5 \text{ m} \times 20 \text{ Hz} = 10 \text{ m/s}$$

b) The period is:
$$T = \frac{1}{f} = \frac{1}{20 \text{ Hz}} = 0.05 \text{ s}$$

c) The angular frequency is:
$$\omega = 2\pi f = 2\pi \times 20 \text{ Hz} = 125.7 \text{ rad/s}$$

d) The wavenumber is:
$$k = \frac{2\pi}{\lambda} = \frac{2\pi}{0.5 \text{ m}} = 12.57 \text{ rad/m}$$

### Example 2: Standing Waves on a String

**Problem:** A guitar string is 0.65 meters long and has a linear mass density of 0.001 kg/m. If the tension in the string is 80 N, calculate:
a) The speed of waves on the string
b) The fundamental frequency (first harmonic)
c) The frequencies of the second and third harmonics
d) The positions of the nodes for the second harmonic

**Solution:**

Given:
- Length of string ($L$) = 0.65 m
- Linear mass density ($\mu$) = 0.001 kg/m
- Tension ($T$) = 80 N

a) The speed of waves on the string is:
$$v = \sqrt{\frac{T}{\mu}} = \sqrt{\frac{80 \text{ N}}{0.001 \text{ kg/m}}} = \sqrt{80,000 \text{ m}^2/\text{s}^2} = 282.8 \text{ m/s}$$

b) The fundamental frequency (first harmonic) is:
$$f_1 = \frac{v}{2L} = \frac{282.8 \text{ m/s}}{2 \times 0.65 \text{ m}} = 217.5 \text{ Hz}$$

c) The frequencies of the second and third harmonics are:
$$f_2 = 2f_1 = 2 \times 217.5 \text{ Hz} = 435.1 \text{ Hz}$$
$$f_3 = 3f_1 = 3 \times 217.5 \text{ Hz} = 652.6 \text{ Hz}$$

d) For the second harmonic, there is one node in the middle of the string in addition to the nodes at both ends. The positions of the nodes are:
- At $x = 0$ (one end)
- At $x = L/2 = 0.65 \text{ m}/2 = 0.325 \text{ m}$ (middle)
- At $x = L = 0.65 \text{ m}$ (other end)

### Example 3: Interference of Waves

**Problem:** Two coherent sources S₁ and S₂ are separated by a distance of 2.0 meters and emit waves with a wavelength of 0.5 meters. A detector is placed 4.0 meters from S₁ and 5.0 meters from S₂. Determine whether constructive or destructive interference occurs at the detector.

**Solution:**

Given:
- Distance between sources = 2.0 m
- Wavelength ($\lambda$) = 0.5 m
- Distance from S₁ to detector = 4.0 m
- Distance from S₂ to detector = 5.0 m

Step 1: Calculate the path difference.
$$\Delta r = r_2 - r_1 = 5.0 \text{ m} - 4.0 \text{ m} = 1.0 \text{ m}$$

Step 2: Express the path difference in terms of wavelengths.
$$\frac{\Delta r}{\lambda} = \frac{1.0 \text{ m}}{0.5 \text{ m}} = 2$$

Step 3: Determine the type of interference.
- Constructive interference occurs when $\frac{\Delta r}{\lambda} = 0, 1, 2, 3, ...$
- Destructive interference occurs when $\frac{\Delta r}{\lambda} = 0.5, 1.5, 2.5, ...$

Since $\frac{\Delta r}{\lambda} = 2$, which is an integer, constructive interference occurs at the detector.

### Example 4: Doppler Effect

**Problem:** A police car with a siren emitting a frequency of 500 Hz is moving at 30 m/s toward a stationary observer. If the speed of sound in air is 340 m/s, calculate the frequency heard by the observer.

**Solution:**

Given:
- Emitted frequency ($f$) = 500 Hz
- Source velocity ($v_s$) = 30 m/s (toward the observer)
- Speed of sound in air ($v$) = 340 m/s

Since the source is moving toward the observer, we use the formula:
$$f' = f\left(\frac{v}{v - v_s}\right)$$

Substituting the values:
$$f' = 500 \text{ Hz} \times \left(\frac{340 \text{ m/s}}{340 \text{ m/s} - 30 \text{ m/s}}\right) = 500 \text{ Hz} \times \left(\frac{340 \text{ m/s}}{310 \text{ m/s}}\right) = 500 \text{ Hz} \times 1.097 = 548.4 \text{ Hz}$$

Therefore, the observer hears a frequency of 548.4 Hz, which is higher than the emitted frequency, as expected for a source moving toward the observer.

### Example 5: Refraction of Waves

**Problem:** A light wave travels from air ($n_1 = 1.00$) into water ($n_2 = 1.33$). If the angle of incidence is 40°, calculate the angle of refraction.

**Solution:**

Given:
- Refractive index of air ($n_1$) = 1.00
- Refractive index of water ($n_2$) = 1.33
- Angle of incidence ($\theta_1$) = 40°

Using Snell's Law:
$$n_1 \sin \theta_1 = n_2 \sin \theta_2$$

Rearranging to solve for $\theta_2$:
$$\sin \theta_2 = \frac{n_1 \sin \theta_1}{n_2} = \frac{1.00 \times \sin 40°}{1.33} = \frac{0.643}{1.33} = 0.483$$

$$\theta_2 = \sin^{-1}(0.483) = 28.9°$$

Therefore, the angle of refraction is 28.9°. As expected, the light wave bends toward the normal when entering a medium with a higher refractive index.

Wave phenomena are fundamental to our understanding of the physical world, from the everyday experiences of sound and light to the most advanced concepts in quantum physics. By mastering the principles of wave behavior, we gain insight into a wide range of natural phenomena and technological applications. The mathematical framework of wave physics provides a powerful tool for describing and predicting how waves interact with their environment and with each other, forming the foundation for many branches of modern science and engineering.