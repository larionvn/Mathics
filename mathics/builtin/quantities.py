from mathics.builtin.base import (Builtin, Test, MessageException)
from mathics.builtin.randomnumbers import RandomEnv
from mathics.builtin.codetables import valid_canonical_unit
from mathics.builtin.strings import to_regex, anchor_pattern, ToLowerCase
from mathics.core.expression import Expression, String, Integer, Real, Symbol,Number, strip_context



import os
import re
import itertools
from itertools import chain
import heapq
import math

import pint
from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity

class KnownUnitQ(Test):
    
    """
    <dl>
    <dt>'KnownUnitQ[$unit$]'
        <dd>returns True if $unit$ is a canonical unit, and False otherwise.
    </dl>

    >> KnownUnitQ["Feet"]
     = True

    >> KnownUnitQ["Foo"]
     = False
    """
    def test(self, expr):
        def validate(unit):
            try:
                Q_(1, unit)
            except Exception:
                return False
            else:
                return True
            
        return validate(expr.get_string_value().lower())
    
class UnitConvert(Builtin):
    
    """
    <dl>
    <dt>'UnitConvert[$quantity$]'
        <dd>returns the unit associated with the specified $quantity$.
    </dl>

    >> UnitConvert[Quantity[5.2, "miles"], "kilometers"]
     = 13.1966 kilograms

    >> QuantityUnit[Quantity[10, "Meters"]]
     = Meters
     
    >> QuantityUnit[Quantity[{10,20}, "Meters"]
     = {Meters, Meters}
    
    """
    
    def apply(self, expr, toUnit, evaluation):
        'UnitConvert[expr_, toUnit_?StringQ]'
        
        def convert_unit(leaves):
            
            mag = leaves[0]
            unit = leaves[1].get_string_value()
            quantity = Q_(mag, unit)
            converted_quantity =  quantity.to(toUnit.get_string_value().lower())
            
            return Expression("Quantity", converted_quantity.magnitude, toUnit)
            
        if QuantityQ(expr).evaluate(evaluation) == Symbol('True'):
            return convert_unit(expr.leaves)
            
    def apply_1(self, expr, evaluation):
        'UnitConvert[expr_]'
        
        def convert_unit(leaves):
            
            mag = leaves[0]
            unit = leaves[1].get_string_value()
            
            if mag.has_form("List", None):
                
                abc = Expression("List")
                for i in range(len(mag.leaves)):
                    c = Q_(mag.leaves[i], unit).to_base_units()
                    print("c  = ", c)
                    abc.leaves.append(Expression("Quantity", c.magnitude, String(c.units)))
#                 for i in range(len(mag)):
#                     
#                     print("mag1 = ", mag, " unit1 = ", unit)
#                     b = Q_(mag, unit)
#                     print("b1 = ", b)
#                     c =  b.to_base_units()
#                     print("c1 = ", c, "mag  = ", c.magnitude,"unit = ", c.units)
#                     abc.leaves.append(Expression("Quantity", c.magnitude, String(c.units)))
                
                return abc
            else:
                quantity = Q_(mag, unit)
                converted_quantity =  quantity.to_base_units()
                
                return Expression("Quantity", converted_quantity.magnitude, String(converted_quantity.units))
                
        #if QuantityQ(expr).evaluate(evaluation) == Symbol('True'):
        if KnownUnitQ(expr.leaves[1]).evaluate(evaluation) == Symbol('True'):
            print("true")
            return convert_unit(expr.leaves)
            
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
     
    #> Quantity[Meters]
     : Unable to interpret unit specification Meters
     = Quantity[Meters]
    """
    
    attributes = ('HoldRest', 'NHoldRest', 'Protected', 'ReadProtected')
     
    messages = {
        'unkunit': 'Unable to interpret unit specification `1`',
        }
    def validate(self, unit, evaluation):
        if KnownUnitQ(unit).evaluate(evaluation) == Symbol('False'):
            return False
        return True

    def apply_makeboxes(self, mag, unit, f, evaluation):
        'MakeBoxes[Quantity[mag_, unit_?StringQ], f:StandardForm|TraditionalForm|OutputForm|InputForm]'

        if (self.validate(unit, evaluation)):
            abc = unit.get_string_value().lower()
            return Expression(
                'RowBox', Expression('List', mag, " ", abc))
        else:
            return Expression(
                    'RowBox', Expression('List', "Quantity", "[", mag, ",", unit.get_string_value().lower(), "]"))

    def apply_n(self, mag, unit, evaluation):
        'Quantity[mag_, unit_?StringQ]'
        expr = Expression('Quantity', mag, unit)
        
        if(self.validate(unit, evaluation)):
            if(mag.has_form("List", None)):
                abc = Expression("List")
                for i in range(len(mag.leaves)):
                    c = Q_(mag.leaves[i], unit.get_string_value().lower())
                    abc.leaves.append(Expression("Quantity", c.magnitude, String(c.units)))
                    
                return abc
            else:    
                a = Q_(mag, unit.get_string_value().lower())
                print("a = ",a )
                return Expression('Quantity', a.magnitude, String(a.units))
        else:
            return evaluation.message('Quantity', 'unkunit', unit)
        
    def apply_1(self, unit, evaluation):
        'Quantity[unit_]'
        if not isinstance(unit, String):
            return evaluation.message('Quantity', 'unkunit', unit)
        else:
            return self.apply_n(Integer(1), unit, evaluation)
        
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
        
        def validate_unit(unit):
            try:
                b = Q_(1, unit)
                print("b = ",b)
            except Exception:
                return False
            else:
                return True
            
        def validate(leaves):
            if len(leaves) < 1 or len(leaves) > 2:
                return False
            elif len(leaves) == 1:
                #if isinstance(leaves[0], String):
                if validate_unit(leaves[0].get_string_value().lower()):
                    return True
                else:
                    return False
            else:
                if isinstance(leaves[0], Number):
                    #if isinstance(leaves[1], String):
                    if validate_unit(leaves[1].get_string_value().lower()):
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
            evaluation.message('Quantity', 'unkunit', get_unit(expr.leaves))
            
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
            evaluation.message('Quantity', 'unkunit', get_magnitude(expr.leaves))
