"""
=================================
3D.retrieval (3D.retrieval)
=================================

.. currentmodule:: 3D.retrieval

The module containing the core techniques for the multiple doppler 
wind retrieval. The :py:func:`get_dd_wind_field` procedure is the
primary wind retrieval procedure in 3D. It contains the optimization
loop that calls all of the cost functions and gradients in 
:py:mod:`3D.cost_functions` so that the user does not need to know
how to call these functions. 

.. autosummary::
    :toctree: generated/

    get_dd_wind_field
    get_bca
    DDParameters
"""

from .wind_retrieve import get_dd_wind_field
from .wind_retrieve import get_bca
from .wind_retrieve import DDParameters