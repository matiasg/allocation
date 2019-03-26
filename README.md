[![Coverage Status](https://img.shields.io/coveralls/github/matiasg/allocation.svg)](https://coveralls.io/github/matiasg/allocation)
[![Build Status](https://travis-ci.org//matiasg/allocation.svg)](https://travis-ci.org/matiasg/allocation)

Allocation
==========

This software solves the following problem:

    * Assume you have a set of sources S = {s_1,..., s_n} and a set of targets T = {t_1,..., t_m}.
    * Each source object must be assigned one (or more) target object(s).
    * This assignment must satisfy a few rules and, among all assignments satisfying those rules, must
    minimize an objective function.

Let's make it more formal:

    * There is a map *I : S -> N_0* (for instances)
    * There is a map *E : T -> N_0* (for nEeds)
    * For each s in S, there is a subset P(s) of T
    * For each s in S and each t in P(s), there is a real number w(s, t) >= 0.

The problem is to construct a (multi)-map *A : S -> T*, where by multi-map we mean that for each
s in S, A(s) is a subset of T, in such a way that

    * A(s) is a subset of P(s) for each s in S,
    * #(A(s)) = I(s) for each s in S,
    * #(A^{-1}(t)) = E(t) for each t in T (here A^{-1}(t) = {s in S | A(s) contains t})
    * among all such maps, find one which minimizes sum_{s in S, t in A(s)} w(s, t).

This problem does not always have a solution. If it doesn't, find a multi-map A which minimizes both

    * the number of s such that #(A(s)) < I(s) and
    * the number of t such that #(A^{-1}(t)) < E(t).

Again, among all such maps, find the one that minimizes

    * sum_{s in S, t in A(s)} w(s, t).
