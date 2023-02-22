import sys

if sys.version_info < (3, 10):
    from importlib_metadata import EntryPoint, version, entry_points
else:
    from importlib.metadata import EntryPoint, version, entry_points

try:
    __version__ = version("nb-cli")
except Exception:
    __version__ = None