2014-Mar-08
###########


How to test an ensemble
***********************

These are notes on :cite:`shirts_simple_2013`.


Abstract
========

It is often difficult to quantitatively determine if a new molecular
simulation algorithm or software properly implements sampling of the
desired thermodynamic ensemble.

We present some simple statistical analysis procedures to allow
sensitive determination of whether the desired thermodynamic ensemble
is properly sampled.

These procedures use paired simulations to cancel out system dependent
densities of state and directly test the extent to which the Boltzmann
distribution associated with the ensemble (usually canonical,
isobaric−isothermal, or grand canonical) is satisfied.


Introduction
============

Molecular simulations, including both molecular dynamics (MD) and
Monte Carlo (MC) techniques, are powerful tools used to study the
properties of complex molecular systems.

When used to specifically study thermodynamics of such systems, rather
than dynamics, the primary goal of molecular simulation is to generate
uncorrelated samples from the appropriate ensemble as efficiently as
possible.


Bibliography
============

.. bibliography:: refs.bib
   :labelprefix: B
   :filter: docname in docnames
