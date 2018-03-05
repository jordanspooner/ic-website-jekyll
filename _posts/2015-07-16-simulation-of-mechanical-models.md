---
layout: post
title: Designing a Real-Time Physics Engine
---

{% include mathjax %}

*These are some notes for a presentation I gave as part of a high-school physics project. A full report, slides and C++ source code is avialable at the bottom of this page.*

Vectors
-------

The first task in the development of a physics engine is to implement a class for vectors, which have significant applications including (but not limited to) defining the co-ordinates of any point in 3D space, as well as changes in space.

When defining a change in position, using vectors, it can be expressed as the product of two components:

$$\textbf{a} = d\textbf{n}$$

In this case, the vector, $\textbf{a}$ is expressed in terms of its magnitude, $d$ (found by Pythagoras' theorem and notably a scalar value), multiplied by a unit vector, which has magnitude 1 in the direction of motion.

The vector, $\textbf{a}$ may also be multiplied by a scalar (changing the magnitude of a but having no influence on its direction) or added to (or subtracted from) another vector (which will give you the resultant of the two vectors).

Finally, we need to implement a function to find the scalar product of two vectors, say $\textbf{a}$ and $\textbf{b}$, which is given by

$$\textbf{a}\bullet\textbf{b}=\textbf{a}_x \textbf{b}_x+ \textbf{a}_y \textbf{b}_y+ \textbf{a}_z \textbf{b}_z$$ 

The major application of the scalar product is to find the angle between two vectors. It is fairly easily proven, using Pythagoras’ Theorem, that:

$$\theta=\arccos\left(\frac{\textbf{a}\bullet\textbf{b}}{\left|\textbf{a}\right|\times\left|\textbf{b}\right|}\right)$$

where $\theta$ gives the angle between the two vectors.

I also chose to include some other functions, which include the vector and component products of two vectors, as well as a function to find the square of the magnitude (since we can then avoid calling the *sqrt* function, and in many cases we will find the square of the magnitude is sufficient for calculations).

The code that deals with these functions is found in *include/engine/core.h*.

Particle Kinematics
-------------------

We can use Newton's Laws of Motion, which describe, to great accuracy, the motion of a point mass (a particle), in order to simulate a great proportion of movements within our engine. For each particle, we of course need to define its position, velocity and acceleration, all of which are vectors (hence the importance of first defining a class for vectors).

Newton's First Law states that an object will continue with constant velocity unless acted upon by an external force. In reality, however, this is rarely ever the case and in the majority of cases, objects will decelerate due frictional forces. Hence we should also add a fourth property to the particle class, which roughly accounts for the effects of drag (and also prevents objects from accelerating due to mathematical inaccuracy). This property is called *damping* in my engine, and simply removes a proportion of a particle's velocity for each subsequent calculation.

Furthermore, Newton's second law states that the resultant force acting upon an object produces acceleration that is proportional to the object's mass. Hence, we should also include the mass of the particle, meaning we can calculate the acceleration, $\mathbf{a}$, using:

$$\mathbf{a}=\frac{\mathbf{F}}{m}$$

It should be clear from the given equation that the mass of an object should never be 0. Furthermore, there may be cases where an infinite mass is required (some objects will be immovable). Hence, we instead store the inverse of the mass, to rectify these two problems.

We also need to take into account the effect of gravity. Since the acceleration due to gravity, $g$, is constant (roughly equal to $9.8ms^{-2}$), there is no need to calculate the force and then convert it back into an acceleration. Instead, $g$ can just be added directly to the acceleration of each particle. Furthermore, this will allow the value of $g$ to easily be changed, which may be required for certain simulations.

To calculate the velocity, we of course need to find $\int a$ $dt$. Meanwhile, to calculate the change in position (displacement), we, using our previously found velocity, find $\int v$ $dt$.

For this we use the semi-implicit Euler integration method. This means that we take the duration of each frame, and add to the previous velocity the acceleration during that frame:

$$\mathbf{v}_{n+1}=\mathbf{v}_{n}+\mathbf{a}_{n}\Delta t$$

For the new position, however, we use the previously calculated (future) velocity, since this helps to stabilise the displacement:

$$\mathbf{p}_{n+1}=\mathbf{p}_{n}+\mathbf{v}_{n+1}\Delta t$$

(Alternatively, one could implement the (simpler and more intuitive) explicit Euler method - however, it is both numerically unstable without a high sampling rate and also rather inaccurate. If we required more a more accurate simulation (say for a scientific or mathematical investigation), we would be more likely to choose a high-order implementation of the Runge-Kutta methods (of which the Euler method can be thought of as simply a first-order implementation)).

The code responsible for these calculations can be found in *include/engine/particle.h* and *src/particle.cpp*, and with the engine in its current state, the *projectile* simulation will work.

Forces
------

So far, our physics engine is able to simulate gravity and (crudely through the *damping* property) drag. There are of course many other forces that we may wish to simulate (including a more sophisticated and accurate versions of gravity and drag).

We can use D'Alembert's Principle for combining multiple forces. It allows us to represent the resultant of several forces as a single force, found from their vector sum:

$$\mathbf{F}=\sum_{i} \mathbf{F}_{i}$$

This is very easily implemented in our engine by creating a vector object that holds the sum of all forces. Each time through the main update loop, we can then add any new forces that arise.

Since the range of forces that we might need to simulate may be extensive, we can implement a standard interface for all forces, and then deal with specific details later on (this is called polymorphism and is the main benefit of using an object-oriented programming language). The interface, the \`\`force generator", is responsible for adding new forces to our objects and updating them, as well as keeping a registry to store all the different kinds of forces we may wish to implement.

**Gravity**

Before this point, we have always added gravity through applying a constant acceleration. Although this is a perfectly valid method for doing so, we now have the ability to introduce gravity as a force (a much cleaner and more sophisticated implementation). We can introduce a class to generate gravity, such that it has the sole property of the acceleration due to gravity, and calculates the force given the mass of the object:

$$\mathbf{F}=mg$$

A single instance of this class could of course be shared among any number of objects.

**Drag**

Our force generator class is also capable of adding a drag force. Although in reality, drag can be found from

$$F_{D} = \frac{1}{2} \rho \mu^{2} C_{D} A$$

where $\rho$ gives the density of the fluid, $\mu$ the flow velocity relative to the object, $A$ the reference area, and $C_{D}$ the drag coefficient, in reality this is too complex and computationally demanding to be simulated accurately in real time.

Hence in many engines, we find the drag equation is often significantly simplified to give:

$$\mathbf{F}_D = -\mathbf{\hat{v}}(k_1\left|\mathbf{v}\right|+k_2\left|\mathbf{v}\right|^2)$$

where $\mathbf{\hat{v}}$ gives a unit vector in the direction of the velocity, $\left\|\mathbf{v}\right\|$ gives the speed of the object, and $k_1$ and $k_2$ are both constants that determine the strength of the drag force.

Hence, where there is a $k_2$ value, the drag will grow more quickly at higher speeds, as in the case with aerodynamic drag (where doubling the speed will cause the magnitude of the drag to almost quadruple).

I should note that despite the new implementations for gravity and drag using our "force generator", I will continue to use damping for drag and add apply gravity directly as an acceleration in my engine. This is because these will be much more efficient and given our uses for the engine, a more complex simulation of gravity and drag is not required.

Springs
-------

Springs and spring-like objects have many applications in a physics engine. They allow us to connect objects, in addition to simulating soft (deformable) objects, and can also be used for a number of (otherwise very complex) effects, such as cloth effects and for fluids (e.g. water ripples).

We can use Hooke's Law to implement springs and spring-like objects in our engine, which states that:

$$F=kx$$

where $k$ gives the spring constant, $x$ the extension, and $F$ the force.

However, we need to manipulate this law so that we can implement it in our (3-dimensional) physics engine, giving:

$$\mathbf{F}=k(\left|\mathbf{d}\right|-l_0)\mathbf{\hat{d}}$$

where $\mathbf{d}$ gives the distance between the two ends of the spring in vector form.

Although real springs will have a limit of elasticity (beyond which permanent deformation will occur), I choose not to implement this in my engine since it is not required in any of my simulations.

We can introduce springs to our engine through the interface we developed for forces earlier. The generator will obviously require the length of the spring and the spring constant, in addition to a pointer that points to the object to which the spring is connected (or a defined point in space). This means that, unlike for our gravity and drag force generators, unfortunately we cannot reuse this instance for multiple objects (instead a we must define new properties for each given spring/ spring-like object).

**Buoyancy**

The force resulting from the buoyancy of an object can quite easily be found using Archimedes' Principle, which states that it is simply given by the weight of the fluid that has been displaced.

However, using this method exactly would require us to calculate the exact volume of every object suspended in a fluid (which, given irregular shapes, may be complex). This kind of calculation is not required as it is unlikely we will need to find the buoyant forces on objects to a high accuracy. An estimation using springs will likely be sufficient.

We can implement this using Hooke's Law by stating that an object near to the surface of the liquid will experience a force that is proportional to its depth. In reality, this is only true for a partially submerged object with a uniform cross-sectional area. When an object is fully submerged, it will instead experience a constant force, and we can implement this by defining a fixed force that acts on an object should it be below a given depth. Likewise, when the object is above a given depth (such that is likely completely unsubmerged), we need not apply any force.

We can therefore define the force as:

$$F=\begin{cases}0&\text{where }d\leq0\text{ (completely unsubmerged)}\\dv\rho&\text{where }0&lt;d&lt;1\text{ (partially submerged)}\\v\rho&\text{where }d\geq1\text{ (completely submerged)}\end{cases}$$

where $d$ gives the proportion of the object submerged, $v$ gives the volume of the object, and $\rho$ gives the density of the liquid. We can calculate the value of $d$ given the y value of the object, $y$, the y-value of the liquid plane, $y_0$ and h is the height of the object (i.e. $y_0-s$ gives the value below which the object is considered to be completely submerged):

$$d=\frac{y-(y_0+s)}{2s}$$

**Stiff Springs**

It would be possible to simulate all collisions using stiff springs, and many physics engines implement this method (referred to as the "penalty method"). However, it is very difficult to do so. If the spring constants are set to small values, then everything will bounce and the scenarios will look unnatural. Meanwhile, if very high values are chosen, there will be a variety errors, from objects accelerating at significant rates, such that they disappear from view almost instantly, to crashes caused by numerical errors as a result of such large values.

(The reason for this is that as we increase the spring constant, the force applied will of course also increase. We will therefore reach a certain stiffness, where the force applied to the spring will be great enough such that it passes its rest length before the next update. If it is now more compressed than it was originally extended, it will accelerate even faster but now in the opposite direction. At the next update, the spring therefore has a greater extension than it did originally! Clearly, as this cycle continues, an ever greater force will be produced and so the end of the object's position will tend towards a position infinitely far away from its original position. Of course this scenario becomes significantly more likely with a slower frame rate. If we need to implement stiff springs, we could use simple harmonic motion, such that the position of one end of the spring obeys the equation:

$$\mathbf{a}={\frac{k}{m}}\mathbf{p}$$

where $k$ gives the spring constant as before. We can then solve this equation to give an expression that links the object's position to its time, and generate the required force according to this. (Although even this method still has several limitations). For this reason, I have not implemented this functionality in my engine.)

Collisions
----------

The final feature I have chosen to implement in my engine is collision detection and resolving.

The most common method for implementing collision detection is to introduce a function that looks through a set of objects and checks whether any two objects are interpenetrating.

It then has to first resolve the interpenetration before resolving the collision itself (otherwise, if the approach speed is very small, the two objects may become stationary at a point where they are still interpenetrating). Although this is a very simple process with one object interacting with the scenery (we just move the object back in the direction of the contact normal until it no longer overlaps), it becomes very much more complex when we begin to involve multiple objects. Take, for example, a small box colliding with the surface of a planet. If we chose to move each of the objects the same amount to resolve the interpenetration, we would obviously see an unrealistic movement of the planet. Hence instead we instead take the masses of the objects into account, giving:

$$\Delta\mathbf{p}_a=\frac{m_b}{m_a+m_b}d\mathbf{n}$$

and

$$\Delta\mathbf{p}_b=-\frac{m_a}{m_a+m_b}d\mathbf{n}$$

where $d$ gives the interpenetration \`depth' and $\mathbf{n}$ gives the direction of the contact normal.

There are two obvious limitations to our collision detection method so far. The first is a result of high-speed collisions. Where objects are moving very quickly towards each other (especially when combined with a low frame rate), they may simply pass through each other without a collision being detected (since the frame only refreshes after they have passed each other). Even if a collision is detected, if the objects have passed halfway through each other, then they will be seen to have a positive separation speed and so no impulse is generated. This issue is particularly difficult to resolve, and as such is beyond the scope of this paper.

The second limitation occurs when we have two particles which are at rest or with very small velocities. Take a particle resting on the ground. Each frame, a downwards acceleration will be provided due to gravity. Hence the particle interpenetrates with the ground, and an impulse will be applied. This will lead to an unnatural movement of the particle such that it will vibrate and sometimes even experience a significant upwards acceleration. This issue is much easier to solve. We simply work out the velocity produced by acceleration and remove it from the velocity we use in our collision resolution. A more sophisticated approach would be to simulate the normal reaction force of the ground on any object. However, when considering irregularly-shaped objects/ ground, one can see this very quickly becomes a complex and difficult task.

There are multiple widely-used methods for implementing collision resolving (such as the penalty method, as mentioned earlier), however I will use an impulse-based solution. First of all, we assume that momentum will always be conserved:

$$m_a\mathbf{u}_a+m_b\mathbf{u}_b=m_a\mathbf{v}_a+m_b\mathbf{v}_b$$

We can then calculate the resulting (separation) velocities following a collision using the equation:

$$v=eu$$

where $v$ gives the separation speed (following the collision), $u$ gives the approach speed (prior to the collision) and $e$ gives the coefficient of restitution between the two colliding objects. We can alter this coefficient to give more elastic ($e\approx1$) or inelastic ($e\approx0$) collisions.

We now use the new separation velocity we found earlier to calculate new velocities given the masses of the involved particles - by equating impulses. The impulse is simply the change in momentum of an object, and it is calculated by the equation:

$$j=m\mathbf{v}-m\mathbf{u}$$

We also need to take into account the direction of the impulse produced. Where we have two particles, we can find the contact normal by considering their positions:

$$\mathbf{\hat{n}}=\widehat{\mathbf{p}_a-\mathbf{p}_b}$$

We keep collisions separate to our other force calculations, instead adding an instantaneous change in velocity each time a collision is detected:

$$\mathbf{v}_{n+1}=\mathbf{v}_{n}+\frac{j}{m}$$

**Rods and Cables**

We can also use the collisions system we have built to introduce rods and cables to our engine. A rod keeps two particles at a given length from each other whilst a cable simply gives a maximum bound of how far apart they can be. The code for implementing these connectors can be found in *pconnector.h* and *pconnector.cpp*.

Simulations
-----------

We now have a fairly complete real-time mass-aggregate physics engine (Sadly, despite having written over 2500 lines of code, I have not yet implemented any physics for rotation or rigid bodies, so more sophisticated simulations involving, for example, objects toppling are not (yet!) possible with my engine.), capable of simulating a wide variety of scenarios. Our final task is to build the actual simulations, so that we can test graphically the engine behaves as expected. A lot of the code required to do so is generic, involving the rendering of 3D graphics (for which I have used OpenGL) and the calculation of the property, *duration*, which gives the time between two frames.

This leaves us only with the task of building the actual applications and giving each of their objects values for the required variables:

***projectile***

![projectile]({{ site.baseurl }}/assets/simulation-of-mechanical-models/projectile.png)

The first simulation, *projectile*, was largely built to test the particle engine developed in Section 2. The code is not especially complex, and there is only one object (apart from the application itself), *projectile1*.

Hence the main task was to provide values for the several variables that are required by the *particle* class. In this case, I have greatly exaggerated the value of $g$ to $20ms^{-2}$. Although it is possible to use the actual value of $g$, $9.8ms^{-2}$, this is rarely ever used in simulations, especially in games where the smaller acceleration can make the simulation less exciting. Given the significant number of approximations and short-cuts we have made during the development of our physics engine so far (in addition to many other factors that we have simply ignored), it would be difficult to achieve a truly realistic simulation, and so in this case I simply chose to select the value of $g$ that gives the best-looking simulation. I have given the projectile a mass of $200kg$ (although this has no effect in this particular simulation - it will be required later for collisions) and a damping factor of 0.99 (i.e. 99% of the projectile's velocity is retained each second), as the air resistance against the projectile is likely to have a very small effect on its acceleration. The angle of projection and initial velocity are defined by the user. This is achieved by the use of a unit vector, multiplied by a magnitude. The user may define the magnitude (within reasonable bounds) and the $y$-value of the unit vector. The $z$ value is then simply calculated to produce a unit vector, using Pythagoras' Theorem (given that $x$ is kept constant).

***springForces***

This simulation demonstrates the spring forces explored in section 4.

***bridge***

The *bridge* simulation makes use of the *pcollision* code (including the use of collisions for cables), discussed in section 5.

Downloads
---------

[Report]({{ site.baseurl }}/assets/simulation-of-mechanical-models/report.pdf)

[Slides]({{ site.baseurl }}/assets/simulation-of-mechanical-models/slides.pdf)

[Annotated Slides]({{ site.baseurl }}/assets/simulation-of-mechanical-models/notes.pdf)
