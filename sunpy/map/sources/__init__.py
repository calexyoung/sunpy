"""Datasource-specific classes

This is where datasource specific logic is implemented. Each mission should
have its own file with one or more classes defined. Typically, these classes
will be subclasses of the :mod`sunpy.map.BaseMap` class.
"""
__all__ = ['sdo', 'soho', 'stereo', 'rhessi']
