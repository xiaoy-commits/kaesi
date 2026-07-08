"""maafw 封装层。

业务代码必须经此模块访问 maafw，禁止直接 import maafw。
"""

from kaesi.maa.facade import MaaFacade, get_facade

__all__ = ["MaaFacade", "get_facade"]