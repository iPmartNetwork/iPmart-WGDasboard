import psutil
import os
import platform

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
        try:
            if platform.system() == "Linux":
                with open('/proc/meminfo') as meminfo_file:
                    for line in meminfo_file:
                        if line.startswith('MemTotal:'):
                            total_ram_kb = int(line.split()[1])
                            return total_ram_kb * 1024  # Convert to bytes
            else:
                return psutil.virtual_memory().total
        except Exception as e:
            print(f"Error retrieving total RAM: {e}")
            return None

    @staticmethod
    def get_used_ram():
        try:
            if platform.system() == "Linux":
                with open('/proc/meminfo') as meminfo_file:
                    meminfo = meminfo_file.read().splitlines()
                data = {line.split(":")[0]: int(line.split()[1]) for line in meminfo if ':' in line}

                total = data.get("MemTotal", 0)
                free = data.get("MemFree", 0)
                buffers = data.get("Buffers", 0)
                cached = data.get("Cached", 0)

                used = (total - free - buffers - cached) * 1024  # Convert to bytes
                return used
            else:
                return psutil.virtual_memory().used
        except Exception as e:
            print(f"Error retrieving used RAM: {e}")
            return None

    @staticmethod
    def get_cpu_capacity():
        try:
            return os.cpu_count()
        except Exception as e:
            print(f"Error retrieving CPU capacity: {e}")
            return None

    @staticmethod
    def get_cpu_usage():
        try:
            return psutil.cpu_percent(interval=0.7)
        except Exception as e:
            print(f"Error retrieving CPU usage: {e}")
            return None

    @staticmethod
    def get_disk_usage():
        try:
            usage = psutil.disk_usage('/')
            return {
                "used": SystemMonitor.format_bytes(usage.used),
                "total": SystemMonitor.format_bytes(usage.total),
                "percent": usage.percent
            }
        except Exception as e:
            print(f"Error retrieving disk usage: {e}")
            return None
