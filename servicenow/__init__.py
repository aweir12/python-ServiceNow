from ._version import get_versions
from .servicenow import ServiceNowInstance
from .operations import (read_table_full)

__version__ = get_versions()['version']
del get_versions
