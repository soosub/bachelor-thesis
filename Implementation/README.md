## pyQuil QAOA implementation for Maxcut
Useful [link](https://grove-docs.readthedocs.io/en/latest/qaoa.html). The pyQuil QAOA class is quite straighforward. You can input a graph, p and an optimization method, the rest is taken care of.

## Qiskit QAOA implementation for Maxcut
I used [this](https://github.com/Qiskit/qiskit-aqua#Optimization) as example 

Useful webpages
- [QAOA](https://qiskit.org/documentation/stubs/qiskit.aqua.algorithms.QAOA.html)
- [Qasm simulator](https://qiskit.org/documentation/stubs/qiskit.providers.aer.QasmSimulator.html)
- [Noise Model](https://qiskit.org/documentation/apidoc/aer_noise.html)
- [Optimizers](https://qiskit.org/documentation/apidoc/qiskit.aqua.components.optimizers.html)


A list of available optimizers (necessary for `QAOA(qubit_op, optimizer, p=p)`) can be found [here](https://qiskit.org/documentation/apidoc/qiskit.aqua.components.optimizers.html), in the module `qiskit.aqua.components.optimizers`. Note, in the example they used the Simultaneous Perturbation Stochastic Approximation (SPSA) optimizer. In the first Rigetti experiments I used Nelder-Mead, make sure you use the *same* optimizer for a fair comparison.

Aqua also contains a lot of other interesting (quantum) algorithms, have a look [here](https://qiskit.org/documentation/apidoc/qiskit.aqua.algorithms.html#module-qiskit.aqua.algorithms)!
