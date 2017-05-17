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
    
    #> Quantity[10, Meters]
     = Quantity[10, Meters]
    """
    
    attributes = ('HoldRest', 'NHoldRest', 'Protected', 'ReadProtected')
    
    rules = {
        'Quantity[unit_?StringQ]':'Quantity[1, unit]',
        }
    
    # def apply_n(self, mag, unit, evaluation):
    #     'Quantity[mag_, unit_?StringQ]'
    #
    #     print("yes, mag = ", mag,"unit = ", unit)
    #     result = String(mag * unit)
    #     b = String(unit)
    #     print("dddd = ", result)
    #     return  String(str(mag.get_int_value()) + " " + unit.get_string_value())

    def validate(self):
        pass

    def apply_makeboxes(self, mag, unit, f, evaluation):
        'MakeBoxes[Quantity[mag_, unit_], f:StandardForm|TraditionalForm|OutputForm|InputForm]'

        if not (self.validate()):
            print("hello")
            return Expression(
                'RowBox', Expression('List', mag, " ", unit))
        else:
            print("aaaa")
            return Expression(
                    'RowBox', Expression('List', "Quantity", "[", mag, ",", unit, "]"))

    def apply_n(self, mag, unit, evaluation):
        'Quantity[mag_, unit_?StringQ]'
        expr =  Expression('Quantity', 1, "Meter")
        if (1): 
            print("going...")
            return expr
        
class QuantityQ(Test):
    """
    <dl>
    <dt>'QuantityQ[$expr$]'
        <dd>return True if $expr$ is a valid Association object, and False otherwise.
    </dl>
    >> QuantityQ[<|a -> 1, b :> 2|>]
     = True
    >> QuantityQ[<|a, b|>]
     = False
    """

    def test(self, expr):
        def validate(leaves):
            for leaf in leaves:
                if leaf.has_form(('Rule', 'RuleDelayed'), 2):
                    pass
                elif leaf.has_form('List', None) or leaf.has_form('Association', None):
                    if validate(leaf.leaves) is not True:
                        return False
                else:
                    return False
            return True

        return expr.get_head_name() == 'System`Quantity' and validate(expr.leaves)
        
class QuantityUnit(Builtin):
    """
    <dl>
    <dt>'QuantityUnit[$magnitude$, $unit$]'
        <dd>represents a quantity with size $magnitude$ and unit specified by $unit$.
    <dt>'QuantityUnit[$unit$]'
        <dd>assumes the magnitude of the specified $unit$ to be 1.
    </dl>

    >> QuantityUnit[Quantity["Kilogram"]]
     = 1 kilogram

    >> QuantityUnit[Quantity[10, "Meters"]]
     = 10 meters
     
    >> QuantityUnit[Quantity[{10,20}, "Meters"]
     = {10 meters, 20 meters}
    
    #> QuantityUnit[Quantity[10, Meters]]
     = Quantity[10, Meters]
    """
    
    def apply(self, expr, evaluation):
        'QuantityUnit[expr_]'
        sympy_expr = expr.to_sympy()
        print("sympy = ", sympy_expr)
        if sympy_expr is None:
            return Expression('List', None)
        return Expression('List', 1, 2)