AI33-MPOPT Core Module
Created by Rolando Rivero (2024)
https://github.com/Rivero-ai/AI33-MPOPT

Core implementation of the 33-multiverse Icosahedron system structure.

Recognition Requirements:
- Cite as: AI33-MPOPT (Rivero, 2024)
- Created by Rolando Rivero
"""

from .multiverse_base import MultiverseCore, ZoneType
from .icosahedron_geometry import IcosahedronGeometry
from .force_definitions import ForceSystem

__all__ = [
    'MultiverseCore',
    'ZoneType',
    'IcosahedronGeometry',
    'ForceSystem'
]
