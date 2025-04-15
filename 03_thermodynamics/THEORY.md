### Derivation of TDEP Free Energy

Given two Hamiltonians $\mathcal{H}_0$ and $\mathcal{H}_1$ we can define $\mathcal{H}(\lambda)$ as the linear mixture of $\mathcal{H}_0$ and $\mathcal{H}_1$:

$$\mathcal{H}(\lambda) = (1-\lambda)\mathcal{H}_0 + \lambda\mathcal{H}_1$$

To get at the free energy, $F$, we can use the fundamental relationship between the partition function, $Z$ and the free energy.
$$Z(\lambda) = \int\exp(-\beta\mathcal{H}(\lambda))d\vec{r}d\vec{p}$$
$$F(\lambda) = -k_{\text{B}}T\log(Z(\lambda)) = -k_{\text{B}}T\log\left(\int\exp(-\beta\mathcal{H}(\lambda))d\vec{r}d\vec{p}\right)$$

Next we expand $F(\lambda)$ about $\lambda = 0$ to get,

$$F(\lambda) = F(0) + \lambda F^\prime(0) + \mathcal{O}(\lambda^2)$$

The first term $F(0)$ is simply,
```math
F(0) \equiv F_0 = -k_{\text{B}}T\log\left(\int\exp(-\beta\mathcal{H}_0)d\vec{r}d\vec{p}\right)
```
the second term is a bit more involved but easy to calculate:
```math
F^\prime(\lambda) = -k_{\text{B}}T\frac{Z^\prime(\lambda)}{Z(\lambda)}
```
```math
Z^\prime(\lambda) = -\beta\int\exp(-\beta\mathcal{H}(\lambda))\frac{\partial\mathcal{H}(\lambda)}{\partial\lambda}d\vec{r}d\vec{p} = -\beta\int\exp(-\beta\mathcal{H}(\lambda))(\mathcal{H}_1 - \mathcal{H}_0)d\vec{r}d\vec{p}
```

Plugging in $\lambda = 0$ we get an intergral in the familiar form of an ensemble average. Importantly, this ensemble average is with respect to Boltzmann weights defined by $\mathcal{H}_0$.
```math
F^\prime(0) = \frac{\int(\mathcal{H}_1 - \mathcal{H}_0)\exp(-\beta\mathcal{H}_0)d\vec{r}d\vec{p}}{\int\exp(-\beta\mathcal{H}_0)d\vec{r}d\vec{p}} = \langle \mathcal{H}_1 - \mathcal{H}_0 \rangle_0
```

So our Taylor-Series expansion is,
```math
F(\lambda) = F_0 + \lambda\langle \mathcal{H}_1 - \mathcal{H}_0 \rangle_0 + \mathcal{O}(\lambda^2)
```

To get a relationship between $F_1$ and $F_0$ we can use the fundamental theorem of calculus,
```math
\begin{align}
\nonumber
F_1 - F_0 &= \int_0^1\frac{\partial F(\lambda)}{\partial\lambda}d\lambda \\
\nonumber
&= \int_0^1\left(\langle \mathcal{H}_1 - \mathcal{H}_0 \rangle_0 + \mathcal{O}(\lambda)\right)d\lambda \\
\nonumber
&= \langle \mathcal{H}_1 - \mathcal{H}_0 \rangle_0 + \cdots
\end{align}
```

If we expand about $\lambda = 1$ instead, we would find that first term is now an esemble average with respect to $\mathcal{H}_1$.

$$F_1 - F_0 =  \langle \mathcal{H}_1 - \mathcal{H}_0 \rangle_1 + \cdots$$

### sTDEP vs MD-TDEP

There are two flavors of TDEP, MD-TDEP and sTDEP. In MD-TDEP samples are generated from an MD trajectory with correct (classical) Boltzmann weights whereas in sTDEP configurations are sampled from a harmonic distribution (e.g., the `canonical_configurations` command).



To recover the TDEP free energy, $F^{\text{TDEP}}$, we take $\mathcal{H}_1$ as the MD Hamiltonian and $\mathcal{H}_0$ to be the TDEP model Hamiltonian expanded to second-order. The kinetic energy for each Hamiltonian is identical, so only the potential energy parts, $V$, matter. As done in the derivation we will truncate the free energy correction to only the first order term. Extra terms can in principle be derived.

In MD-TDEP we sample with respect to the true distribution so we should use the free energy expansion in terms of $\langle\cdot\rangle_1$ to find that,

```math
\begin{align}
F^{\text{MD}} \approx F^{\text{MD-TDEP}} &= F^{\text{TDEP}}_0 + \langle V_{\text{MD}} - V_{\text{TDEP}} \rangle_{\text{MD}}\\
&= F^{\text{TDEP}}_0 + \langle V_{\text{MD}} - V_2 \rangle_{\text{MD}}
\end{align}
```

with $F^{\text{TDEP}}_0$ the free energy of a system of harmonic oscillators with tempearture dependent frequencies from the TDEP. In sTDEP we need the expansion in terms of $\langle\cdot\rangle_0$ and find that
```math
F^{\text{sTDEP}} = F^{\text{TDEP}} _0 + \langle V_{\text{MD}} - V_2 \rangle_{\text{Harmonic}}
```


Note that we are only able to use a harmonic potential for $\mathcal{H}_0$ as we do not have a closed form expression for $F_0$ with anharmonic terms.
