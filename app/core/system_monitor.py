
import psutil
import os

class SystemMonitor:
    @staticmethod
    def format_bytes(bytes_value):
        if bytes_value < 1024:
            return f"{bytes_value} B"
        elif bytes_value < 1024 ** 2:
            return f"{bytes_value / 1024:.2f} KB"
        elif bytes_value < 1024 ** 3:
            return f"{bytes_value / (1024 ** 2):.2f} MB"
        else:
            return f"{bytes_value / (1024 ** 3):.2f} GB"

    @staticmethod
    def get_total_ram():
        with open('/proc/meminfo') as meminfo_file:
            for line in meminfo_file:
                if line.startswith('MemTotal:'):
                    total_ram_kb = int(line.split()[1])
                    return total_ram_kb

    @staticmethod
    def get_used_ram():
        with open('/proc/meminfo') as meminfo_file:
            meminfo = meminfo_file.read().splitlines()
        data = {line.split(":")[0]: int(line.split()[1]) for line in meminfo if ':' in line}

        total = data.get("MemTotal", 0)
        free = data.get("MemFree", 0)
        buffers = data.get("Buffers", 0)
        cached = data.get("Cached", 0)

        used = total - free - buffers - cached
        return used

    @staticmethod
    def get_cpu_capacity():
        return os.cpu_count()

    @staticmethod
    def get_cpu_usage():
        return psutil.cpu_percent(interval=0.7)

    @staticmethod
    def get_disk_usage():
        usage = psutil.disk_usage('/')
        return f"{SystemMonitor.format_bytes(usage.used)} / {SystemMonitor.format_bytes(usage.total)}"
