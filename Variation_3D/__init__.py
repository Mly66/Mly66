"""
========================================
3D: Variation_3D
========================================
"""

from . import cost_functions
from . import retrieval
from . import vis
from . import initialization
from . import tests
from . import constraints

__version__ = '1.2.0'

# print("Welcome to 3D %s" % __version__)
# print("Detecting Jax...")
try:
    import jax
    # print("Jax engine enabled!")
except ImportError:
    pass
    # print("Jax is not installed on your system, unable to use Jax engine.")

# print("Detecting TensorFlow...")
try:
    import tensorflow
    print("TensorFlow detected.")
    import tensorflow_probability
    print("TensorFlow-probability detected. TensorFlow engine enabled!")
except (ImportError, AttributeError) as e:
    # print("Unable to load both TensorFlow and tensorflow-probability. " +
    #         "TensorFlow engine disabled.")
    # print(e)
    pass

