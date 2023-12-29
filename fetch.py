import asyncio
import platform
import psutil
import socket
import requests
import subprocess
from termcolor import colored

async def get_local_ip():
    try:
        local_ip = "• " + colored("Local IP", "red") + ": {0}".format(socket.gethostbyname(socket.getfqdn()))
    except Exception as e:
        local_ip = "• " + colored("Local IP", "red") + ": Error - " + str(e)
    return local_ip

async def get_global_ip():
    try:
        global_ip = "• " + colored("Global IP", "red") + ": {0}".format(await get_global_ip_async())
    except Exception as e:
        global_ip = "• " + colored("Global IP", "red") + ": Error - " + str(e)
    return global_ip

async def get_global_ip_async():
    async with aiohttp.ClientSession() as session:
        response = await session.get('https://api.ipify.org')
        return await response.text()

def get_os_info():
    try:
        OS_raw = subprocess.getoutput("lsb_release -d")
    except Exception as e:
        OS_raw = f"Error - {str(e)}"

    os_info = "• " + colored("OS", "red") + ": {0}".format(OS_raw)
    return os_info

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

def get_package_manager_info():
    # Detect additional package managers here
    flatpak_info = subprocess.getoutput("flatpak --version")
    snap_info = subprocess.getoutput("snap --version")
    pacman_info = subprocess.getoutput("pacman --version")

    package_manager_info = []
    if "flatpak" in flatpak_info:
        package_manager_info.append("• " + colored("Flatpak", "red") + f": {flatpak_info}")
    if "snap" in snap_info:
        package_manager_info.append("• " + colored("Snap", "red") + f": {snap_info}")
    if "Pacman" in pacman_info:
        package_manager_info.append("• " + colored("Pacman", "red") + f": {pacman_info}")

    return package_manager_info

def get_network_info():
    local_ip_task = asyncio.create_task(get_local_ip())
    global_ip_task = asyncio.create_task(get_global_ip())

    local_ip, global_ip = await asyncio.gather(local_ip_task, global_ip_task)
    return local_ip, global_ip

def get_kernel_info():
    kernel_info = "• " + colored("Kernel Version", "red") + ": {0}".format(platform.uname().release)
    return kernel_info

def get_uptime_info():
    uptime = subprocess.getoutput('uptime -p').replace("up ", "")
    uptime_info = "• " + colored("Uptime", "red") + ": {0}".format(uptime)
    return uptime_info

async def main_async():
    os_info = get_os_info()
    cpu_info = get_cpu_info()
    memory_info, swap_info = get_memory_info()
    storage_info = get_storage_info()
    battery_info = get_battery_info()
    network_info = await get_network_info()
    kernel_info = get_kernel_info()
    uptime_info = get_uptime_info()
    dpkg_info = get_package_manager_info()

    # Print system information
    print(os_info)
    print(cpu_info)
    print(memory_info)
    print(swap_info)
    print(storage_info)
    print(battery_info)
    print("Local IP:", network_info[0])
    print("Global IP:", network_info[1])
    print(kernel_info)
    print(uptime_info)
    for pm_info in dpkg_info:
        print(pm_info)

if __name__ == "__main__":
    import aiohttp

    # Run the asynchronous main function
    asyncio.run(main_async())
