from mathics.builtin.base import Builtin, MessageException
from mathics.builtin.randomnumbers import RandomEnv
from mathics.builtin.codetables import unit_short_term
from mathics.builtin.strings import to_regex, anchor_pattern
from mathics.core.expression import Expression, String, Integer, Real, Symbol, strip_context

import os
import re
import itertools
from itertools import chain
import heapq
import math


class Quantity(Builtin):
    """
    <dl>
    <dt>'Quantity[$magnitude$, $unit$]'
        <dd>represents a quantity with size $magnitude$ and unit specified by $unit$.
    <dt>'Quantity[$unit$]'
        <dd>assumes the magnitude of the specified $unit$ to be 1.
    </dl>

    >> Quantity["Kilogram"]
     = 1 kilogram

    >> Quantity[10, "Meters"]
     = 10 meters
     
    >> Quantity[{10,20}, "Meters"
     = {10 meters, 20 meters}


    """
    
    attributes = (HoldRest, NHoldRest, Protected, ReadProtected)
    
    def apply_n(self, expr, n, evaluation):
        'Quantity[expr_, mag_, unit_]'

        if expr.is_atom():
            evaluation.message('Tuples', 'normal')
            return
        n = n.get_int_value()
        if n is None or n < 0:
            evaluation.message('Tuples', 'intnn')
            return
        items = expr.leaves

        def iterate(n_rest):
            evaluation.check_stopped()
            if n_rest <= 0:
                yield []
            else:
                for item in items:
                    for rest in iterate(n_rest - 1):
                        yield [item] + rest

        return Expression('List', *(Expression(expr.head, *leaves)
                                    for leaves in iterate(n)))