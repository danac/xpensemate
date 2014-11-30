#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2014 Dana Christen
#
# This file is part of XpenseMate, a tool for managing shared expenses and
# hosted at https://github.com/danac/xpensemate.
#
# XpenseMate is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""
This module contains code used to format and compare floating-point numbers,
in particular monetary amounts.
"""

def round_to_closest_multiple(amount, multiple):
    """
    Round a value to the closest multiple of a given number. Useful to round
    an amount to the smallest monetary unit (e.g. 5 cents).
    
    :param float amount: The value to round
    :param float multiple: The number to the closest multiple of which
        the value must be rounded
    :rtype: float
    """
    
    return round(float(amount)/float(multiple))*float(multiple)
    

def format_amount(amount, smallest_unit):
    """
    Properly format a monetary for display amount
    based on a given smallest amount.
    
    :param float amount: The value to format
    :param float smallest_unit: The number to the closest multiple of which
        the value must be rounded
    :rtype: str
    """
    
    # Ok it's a bit dirty, but it works perfectly for standard cases
    precision = len(str(smallest_unit).split('.')[1])
    placeholder = '{{:.{}f}}'.format(precision)
    return placeholder.format(round_to_closest_multiple(amount, smallest_unit))
    

