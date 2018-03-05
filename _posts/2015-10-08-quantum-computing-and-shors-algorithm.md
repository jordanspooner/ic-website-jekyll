---
layout: post
title: Quantum Computing and Shor's Algorithm
---

*These are some notes I prepared for a talk for the Judd School Computer Science Society. The slides are available at the bottom of the page.*

{% include mathjax %}

Quantum Computing
-----------------

Quantum computers utilise the laws of quantum mechanics, giving them entirely different properties to classical computers (as we will see). For this reason, we will first need to discuss quantum mechanics:

Contrary to GCSE Physics/ Chemistry, electrons do not orbit around the nucleus like the Earth orbits around the Sun. In fact, electrons have no definite position or velocity - it's a smear of a probability wave, until that electron is observed.

However, whilst we don't know where an electron is, we can work out a probability - by using a property called the amplitude. The amplitude can be positive, negative, or even imaginary, and the probability is given simply by the square of the amplitude. The probabilities should sum to 1 as we would expect. So a quantum weather forecaster might (not very helpfully) say "there's a $1/\sqrt{2}$ chance of rain tomorrow and a $-1/\sqrt{2}$ chance of clear weather." Formally, given a quantum state, $\psi = \alpha \langle0\rangle + \beta \langle1\rangle$ (where $\alpha$ and $\beta$ are amplitudes), we would have the conditions $\alpha , \beta \in \mathbb{C}$ and $\alpha ^2 + \beta ^2 = 1$.

![qstates]({{site.baseurl}}/assets/quantum-computing-and-shors-algorithm/qstates.png)

We can draw a graph using the properties of an electron (usually spin). Given $\alpha ^2 + \beta ^2 = 1$, we will of course end up with a circle. Each point on the circumference is a possible quantum state. When the electron is observed, the quantum state is forced into a horizontal or vertical line. The closer the quantum state is to $\langle0\rangle$, the more likely it is to be observed as $\langle0\rangle$ (down spin). From then on, it will always have a down spin when observed (as long as we don't do anything with our electron in between consecutive observations); we have essentially changed its state.

Note, however, that 'choosing' a quantum state is fundamentally different from flipping a coin. When we flip a coin, the outcome is unknown due to probability (there's a half chance of tails and a half chance of heads) and ignorance (we haven't looked at the coin yet). In contrast, we don't know the properties of an electron due to intrinsic randomness. We can prove this by taking an electron observed in the $\langle0\rangle$ state. Say we find some function that 'moves the state diagonally right and upwards'. As long as we don't observe the electron after performing this process once, we will always end up with an electron in the $\langle1\rangle$ state after performing the action twice (note how this is different to flipping coins!).

An easy way to understand this is through interference. We can define two rules that will always hold for the function we described earlier, which are $\langle0\rangle \rightarrow \langle0\rangle/\sqrt{2} + \langle1\rangle/\sqrt{2}$ and $\langle1\rangle \rightarrow -\langle0\rangle/\sqrt{2} + \langle1\rangle/\sqrt{2}$ (try testing these rules out for the cases described earlier if you want proof they work!). So we can see that the $\langle0\rangle$ paths would interfere and cancel out, leaving only the $\langle1\rangle$ paths. Some like to think of these paths as 'parallel universes'.

![interference]({{site.baseurl}}/assets/quantum-computing-and-shors-algorithm/interference.png)

Now we finally have enough background knowledge that we can start to apply quantum mechanics to computation! If we had 2 classical bits, we have four possibilities of 00,01,10 and 11.

If we had 2 quantum bits, we again have four possibilities which are the three triplet states (having a total spin of 1) and the one singlet state, $s$, which has 0 spin.

![qubits]({{site.baseurl}}/assets/quantum-computing-and-shors-algorithm/qubits.png)

$\langle0,1\rangle$ and $\langle1,0\rangle$ are not stable states on their own (we can have a state of 1 up electron and 1 down electron, but we cannot tell which is which - we only know the property that they are opposites). You can think of this like a coupled pendulum: if we set the pendulums in motion in opposite directions, their velocities will always be opposite to each other, but they are constantly changing.

But we can form a superposition using these entangled states: one option is where they are 'in phase' - both have positive amplitude (the $T_0$ state) and the other is where they are 'in antiphase' - one has positive amplitude and the other has negative amplitude (the $s$ state). Importantly, qubits are not independent of each other: in this case, as soon as one is observed, the other is immediately determined to be the opposite.

The power of quantum computing comes from the possible superpositions, since whilst 1 bit stores 1 value, 1 qubit holds two values, $\alpha$ for the amplitude of the $\langle0\rangle$ state and $\beta$ for the amplitude of the $\langle1\rangle$ state. With 2 qubits, we now have 4 values: $\alpha \langle0\rangle, \beta \langle T_0\rangle, \gamma \langle s\rangle, \delta \langle1\rangle$. We can see that whilst $n$ classical bits hold $n$ values, $n$ qubits hold $2^n$ values. This means with as few as 300 qubits in a fully-entangled space (i.e. all superpositions are possible), we can hold the equivalent of $2^{300}$ classical bits of information (more bits than there are particles in the universe!).

Quantum computing does have a few problems though. Firstly, quantum computers are only faster where a fast quantum algorithm exists (e.g. for the prime factorisation problem). Using classical algorithms, quantum computers are unlikely to be faster than classical computers, and in fact will likely be slower. Furthermore superpositions are fickle in that they are easily disrupted and have a short coherence times. Finally, we must define all algorithms such that our end result is a basis state. If we end up with a complex superposition, we cannot measure the result (observing the result will cause the loss of our superposition).

Shor's Algorithm
----------------

Shor's algorithm is a quantum algorithm for solving the quantum prime factorisation problem. The problem is to find the two prime factors of an often very large number. It's an $O(e^{(\log n \log \log n)^{1/2}})$ (sub exponential) problem using classical algorithms, yet Shor's algorithm solves it in polynomial time (as of 2012, the largest number prime factorised by Shor's Algorithm is 56 153). It is also the problem on which the popular RSA cryptosystem is based.

Shor's algorithm is made up of first a classical part, in which we redefine the prime factorisation problem to an order solving problem, and then a quantum part, in which we solve that order finding problem. We'll start by discussing the classical part: 

Take the sequence of powers of 2:

$$2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, …$$

Now if we take the above sequence mod 15:

$$2, 4, 8, 1, 2, 4, 8, 1, 2, 4, …$$

We get a sequence with a period of 4.

Now with mod 21:

$$2, 4, 8, 16, 11, 1, 2, 4, 8, 16, …$$

We get a sequence with a period of 6.

In fact, if we have any sequence, $x \mod N, x^2 \mod N, x^3 \mod N, x^4 \mod N, ...$, then the period will be divisible by $(p-1)(q-1)$ (this is the totient of $N$) where $p$ and $q$ are the prime factors of $N$ (as long as $x$ is not divisible by $p$ or $q$).

So, taking our examples above:

Let $x = 2$ and $N = 15$. In this case, the prime factors are of course $p=3$ and $q=5$. 

$\implies (p-1)(q-1) = 8$. $4 \mid 8$ as required.

Where $x = 2$ and $N = 21$, $p=3$ and $q=7$. 

$\implies (p-1)(q-1) = 12$. $6 \mid 12$ as required.

We could therefore, given an $N$ to factorise, test with multiple values of $x$ to get a good idea of $(p-1)(q-1)$, and then work out the prime factors, $p$ and $q$.

It turns out that the period finding problem, whilst still difficult for a classical computer (the period may be almost as large as $N$!), is a much easier problem for a quantum computer than trying to find prime factors. Rather than looking for 'one possible universe', we are now looking for 'a global property of all possible universes'.

We now need to solve two problems:

-   How to get a superposition over $x \mod N, x^2 \mod N, x^3 \mod N, x^4 \mod N, ...$?
-   What function can we use on that superposition to find the period?

Let’s start with the first problem: We can create a superposition over all integers $r$, from 1 up to $N$, but given that $r$ is very large (hundreds of thousands of digits), we will need to use repeated squaring in order to calculate $x^r \mod N$. We can then apply the $\mod N$ at each stage, ensuring our numbers don't get too large: 

e.g. Let $N=17$, $x=3$, $r=14=2^3+2^2+2^1$

$\implies x^r = x^{2^3+2^2+2^1} = 3^{2^3} \times 3^{2^2} \times 3^{2^1} = (3^2)^2)^2 \times (3^2)^2 \times 3^2$ 

$\implies x^r \mod N =6561 \mod 17 \times 81 \mod 17 \times 9 \mod 17$ 

$= (16 \times 13 \times 9) \mod 17 = 2$ 

Now onto the second problem - how do we find the period? 

We use something called the quantum fourier transform (QFT). We will explain how this works through an example (this heavily simplified explanation isn't my own, but is taken from Scott Aaronson's excellent [blog post](http://www.scottaaronson.com/blog/?p=208)) – during the holidays, being a mathematician with no friends, sometimes I start to live a 26 hour day. One day I wake up at 9, the next at 11, the next at 1pm and so on.

So say I wake up one day at 5pm – what can you tell about my schedule – not much except that I’m probably not living a 24 hour day!

Instead, imagine I have a wall of clocks, each with a different time period – one for 23hr, one for 24, one for 26.3 and so on. Beneath each clock is a posterboard with a thumbtack – now each day, I move the thumbtack a centimetre in the direction of the hour hand of the clock above it. We should now be able to tell more about my schedule: if I’m on a 26 hour day, all the thumbtacks except for the 26 hour one will undergo periodic motion – whilst the 26 hour thumbtack will move the same direction every day – soon it will be off the posterboard!

![shor]({{site.baseurl}}/assets/quantum-computing-and-shors-algorithm/shor.png)

That essentially is what the QFT is – it is a linear (indeed a unitary) transformation which maps one vector of complex numbers to another vector of complex numbers.

The input vector has a non-zero entry corresponding to each time I wake up (each of the numbers in our sequence), and zero entries everywhere else.

The output vector records the positions of the thumbtacks on the posterboards (points on the complex plane). 

Mathematically, the fourier transform takes a function of time, and finds its constituent frequencies – the QFT essentially does the same thing but to the vector of amplitudes of a quantum state (for a much more in depth explanation, I would recommend these [lecture notes](http://www.cs.bham.ac.uk/internal/courses/intro-mqc/current/) from the University of Birmingham, which are both detailed and fairly easy to understand).

So we have a transformation that maps a quantum state encoding a periodic sequence, to a quantum state encoding the period of that sequence.

Earlier, we discussed how interference is the key concept in quantum mechanics that we are interested in. Amplitudes can be positive negative, or even complex – because of this amplitudes can interfere destructively and cancel each other out. This is what happens in Shor's algorithm. All of the periods other than the true give values pointing in different directions, which cancel each other out. Only for the true period will all the contributions point in the same direction (constructive interference) – so our final result is the true period with high probability.

Resources
---------

[Lecture Slides]({{site.baseurl}}/assets/quantum-computing-and-shors-algorithm/slides.pdf)

References
----------

*Scott Aaronson* [Shor, I'll do it](http://www.scottaaronson.com/blog/?p=208)

*Scott Aaronson* [The Limits of Quantum](http://www.cs.virginia.edu/~robins/The_Limits_of_Quantum_Computers.pdf)

*Scott Aaronson* [Quantum Computing for High School Students](http://www.scottaaronson.com/writings/highschool.html)

*Ronald de Wolf* [Quantum Computing: Lecture Notes](http://homepages.cwi.nl/~rdewolf/qcnotes.pdf)

*Andrea Morello* [How does a Quantum Computer Work?](https://www.youtube.com/watch?v=g_IaVepNDT4)

*Michelle Simmons* [Quantum Computation](https://www.youtube.com/watch?v=cugu4iW4W54)

*Iain Styles, Jon Rowe* [Introduction to Molecular and Quantum Computation](http://www.cs.bham.ac.uk/internal/courses/intro-mqc/current/)

*Nicolas Wöhrl* [Introduction to Quantum Computers](https://www.youtube.com/watch?v=Fb3gn5GsvRk)
