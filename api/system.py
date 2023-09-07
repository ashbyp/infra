from platform import platform
from typing import Any

import psutil, os, socket,  platform

from api.API import API


class SystemAPI(API):

    def get_status(self) -> dict[str, Any]:
        status = {
            "pid": os.getpid(),
            "process_name": psutil.Process(os.getpid()).name(),
            "hostname": socket.gethostname(),
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "platform_system": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "platform": platform.platform(),
            "cpu_percent": psutil.cpu_percent(),
            "cpu_time": psutil.cpu_times(),
            "virtual_memory": psutil.virtual_memory(),
        }
        super().called()
        return status

    def ping(self) -> str:
        super().called()
        return f'pid: {os.getpid()}'

