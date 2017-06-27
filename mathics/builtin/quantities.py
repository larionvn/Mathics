from mathics.builtin.base import (Builtin, Test, MessageException)
from mathics.builtin.randomnumbers import RandomEnv
from mathics.builtin.codetables import unit_short_term
from mathics.builtin.strings import to_regex, anchor_pattern, ToLowerCase
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
     
    >> Quantity[{10,20}, "Meters"]
     = {10 meters, 20 meters}
    
    #> Quantity[10, Meters]
     = Quantity[10, Meters]
    """
    
    attributes = ('HoldRest', 'NHoldRest', 'Protected', 'ReadProtected')
    
    rules = {
        'Quantity[unit_?StringQ]':'Quantity[1, unit]',
        }
    
    messages = {
        'unkunit': 'Unable to interpret unit specification `1`',
        }
    def validate(self):
        pass

    def apply_makeboxes(self, mag, unit, f, evaluation):
        'MakeBoxes[Quantity[mag_, unit_String], f:StandardForm|TraditionalForm|OutputForm|InputForm]'

        if not (self.validate()):
            print("hello")
            return Expression(
                'RowBox', Expression('List', mag, " ", unit.get_string_value().lower()))
        else:
            print("aaaa")
            return Expression(
                    'RowBox', Expression('List', "Quantity", "[", mag, ",", unit, "]"))

    def apply_n(self, mag, unit, evaluation):
        'Quantity[mag_, unit_?StringQ]'
        expr =  Expression('Quantity', mag, unit)
        if (1): 
            print("going...")
            return expr
        
class QuantityQ(Test):
    """
    <dl>
    <dt>'QuantityQ[$expr$]'
        <dd>return True if $expr$ is a valid Association object, and False otherwise.
    </dl>
    
    >> QuantityQ[Quantity[3, "Meters"]]
     = True
    
    >> QuantityQ[Quantity[3, "Maters"]]
     = False
    """

    def test(self, expr):
        def validate(leaves):
            if len(leaves) < 1 or len(leaves) > 2:
                return False
            elif len(leaves) == 1:
                if isinstance(leaves[0], String):
                    return True
                else:
                    return False
            else:
                if isinstance(leaves[0], Integer):
                    if isinstance(leaves[1], String):
                        return True
                    else:
                        return False
                else:
                    return False
            
        return expr.get_head_name() == 'System`Quantity' and validate(expr.leaves)
        
class QuantityUnit(Builtin):
    """
    <dl>
    <dt>'QuantityUnit[$quantity$]'
        <dd>returns the unit associated with the specified $quantity$.
    </dl>

    >> QuantityUnit[Quantity["Kilogram"]]
     = kilograms

    >> QuantityUnit[Quantity[10, "Meters"]]
     = Meters
     
    >> QuantityUnit[Quantity[{10,20}, "Meters"]
     = {Meters, Meters}
    
    """
    
    def apply(self, expr, evaluation):
        'QuantityUnit[expr_]'
        
        def get_unit(leaves):
            if len(leaves) == 1:
                return leaves[0]
            else:
                return leaves[1]
            
        if QuantityQ(expr).evaluate(evaluation) == Symbol('True'):
            print("true")
            return get_unit(expr.leaves)
        else:
            evaluation.message('Quantity', 'unkunit', get_unit(expr.leaves) )
            
class QuantityMagnitude(Builtin):
    """
    <dl>
    <dt>'QuantityMagnitude[$quantity$]'
        <dd>gives the amount of the specified $quantity$.
    <dt>'QuantityMagnitude[$quantity$,$unit$]'
        <dd>gives the value corresponding to $quantity$ when converted to $unit$.
    </dl>
    
    >> QuantityMagnitude[Quantity["Kilogram"]]
     = 1

    >> QuantityMagnitude[Quantity[10, "Meters"]]
     = 10
     
    #> QuantityMagnitude[Quantity[{10,20}, "Meters"]]
     = {10, 20}
    
    #> QuantityMagnitude[Quantity[1, "meter"], "centimeter"]
     = 100
     
    #> QuantityMagnitude[Quantity[3, "mater"]]
     : Unable to interpret unit specification mater.
     = QuantityMagnitude[Quantity[3, mater]]
    """
    
    def apply(self, expr, evaluation):
        'QuantityMagnitude[expr_]'
        
        def get_magnitude(leaves):
            if len(leaves) == 1:
                return 1
            else:
                return leaves[0]
            
        if QuantityQ(expr).evaluate(evaluation) == Symbol('True'):
            print("true")
            return get_magnitude(expr.leaves)
        else:
            evaluation.message('Quantity', 'unkunit', get_magnitude(expr.leaves) )