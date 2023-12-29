import asyncio
import platform
import psutil
import socket
import aiohttp
import subprocess
from termcolor import colored

async def get_os_info():
    try:
        OS_raw = subprocess.getoutput("lsb_release -d")
        OS = OS_raw.replace("Description:", "").strip()
    except Exception as e:
        OS = f"Error - {str(e)}"

    os_info = "• " + colored("OS", "red") + ": {0}".format(OS)
    return os_info

async def get_network_info():
    try:
        local_ip = "• " + colored("Local IP", "red") + ": {0}".format(socket.gethostbyname(socket.gethostname()))
        global_ip = "• " + colored("Global IP", "red") + ": {0}".format(await get_global_ip())
    except Exception as e:
        local_ip = "• " + colored("Local IP", "red") + ": Error - " + str(e)
        global_ip = "• " + colored("Global IP", "red") + ": Error - " + str(e)
    return local_ip, global_ip

async def get_global_ip():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.ipify.org') as response:
                return await response.text()
    except Exception as e:
        return f"Error - {str(e)}"

def get_cpu_info():
    cpu_info = "• " + colored("CPU", "red") + ": {0}".format(platform.processor())
    return cpu_info

def get_memory_info():
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()
    memory_info = "• " + colored("Memory (RAM)", "red") + ": Total: {0} GB, Used: {1} GB ({2}%)" \
        .format(round((ram.total / (1024.0 * 1024 * 1024)), 2), round((ram.used / (1024.0 * 1024 * 1024)), 2), ram.percent)
    swap_info = "• " + colored("Swap Memory", "red") + ": Total: {0} GB, Used: {1} GB ({2}%)" \
        .format(round((swap.total / (1024.0 * 1024 * 1024)), 2), round((swap.used / (1024.0 * 1024 * 1024)), 2), swap.percent)
    return memory_info, swap_info

def get_storage_info():
    storage = psutil.disk_usage('/')
    storage_info = "• " + colored("Storage", "red") + ": Total: {0} GB, Used: {1} GB ({2}%)" \
        .format(round((storage.total / (1024.0 * 1024 * 1024)), 2), round((storage.used / (1024.0 * 1024 * 1024)), 2), storage.percent)
    return storage_info

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery.power_plugged:
        battery_info = "• " + colored("Battery", "red") + f": {battery.percent}% (Charging)"
    else:
        battery_info = "• " + colored("Battery", "red") + f": {battery.percent}% (Discharging)"
    return battery_info

def get_kernel_info():
    kernel_info = "• " + colored("Kernel Version", "red") + ": {0}".format(platform.uname().release)
    return kernel_info

def get_uptime_info():
    uptime = subprocess.getoutput('uptime -p').replace("up ", "")
    uptime_info = "• " + colored("Uptime", "red") + ": {0}".format(uptime)
    return uptime_info

def get_dpkg_info():
    dpkg_packages = subprocess.getoutput("dpkg -l | grep -c ^ii")
    dpkg_info = "• " + colored("Packages", "red") + ": {0} (dpkg)".format(dpkg_packages)
    return dpkg_info

async def main_async():
    # Get system information
    os_info = await get_os_info()
    cpu_info = get_cpu_info()
    memory_info, swap_info = get_memory_info()
    storage_info = get_storage_info()
    battery_info = get_battery_info()

    # Get network information asynchronously
    local_ip, global_ip = await get_network_info()

    # Get kernel information
    kernel_info = get_kernel_info()

    # Get system uptime
    uptime_info = get_uptime_info()

    # Get dpkg package information
    dpkg_info = get_dpkg_info()

    # Print system information
    print(os_info)
    print(cpu_info)
    print(memory_info)
    print(swap_info)
    print(storage_info)
    print(battery_info)
    print(local_ip)
    print(global_ip)
    print(kernel_info)
    print(uptime_info)
    print(dpkg_info)

if __name__ == "__main__":
    asyncio.run(main_async())
