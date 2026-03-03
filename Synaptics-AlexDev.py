#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  Synaptics-Killer v2.0  |  Set By AlexDev                   ║
║  Recovery Tool for XRed Backdoor Infected Files (EXE/XLSX)   ║
║  License: GPL-3.0                                            ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import struct
import shutil
import ctypes
import logging
import zipfile
import datetime
import subprocess
import glob

# ══════════════════════════════════════════════════════════════
#  ANSI Color Constants - Red Theme
# ══════════════════════════════════════════════════════════════

class C:
    """Color codes for terminal output - Red Theme"""
    RESET       = "\033[0m"
    BOLD        = "\033[1m"
    DIM         = "\033[2m"
    ITALIC      = "\033[3m"
    UNDERLINE   = "\033[4m"
    BLINK       = "\033[5m"

    # Red theme palette
    BLACK       = "\033[30m"
    RED         = "\033[31m"
    DARK_RED    = "\033[38;5;124m"
    BRIGHT_RED  = "\033[91m"
    FIRE_RED    = "\033[38;5;196m"
    BLOOD_RED   = "\033[38;5;88m"
    CRIMSON     = "\033[38;5;160m"
    SCARLET     = "\033[38;5;202m"
    ORANGE_RED  = "\033[38;5;208m"
    WHITE       = "\033[97m"
    GRAY        = "\033[90m"
    DARK_GRAY   = "\033[38;5;236m"
    LIGHT_GRAY  = "\033[38;5;245m"
    YELLOW      = "\033[93m"
    GREEN       = "\033[92m"
    CYAN        = "\033[96m"
    MAGENTA     = "\033[95m"

    # Backgrounds
    BG_RED      = "\033[41m"
    BG_DARK_RED = "\033[48;5;52m"
    BG_BLACK    = "\033[40m"
    BG_GRAY     = "\033[48;5;235m"


def enable_ansi_windows():
    """Enable ANSI escape codes on Windows 10+"""
    if os.name == 'nt':
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_terminal_width():
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 80


# ══════════════════════════════════════════════════════════════
#  ASCII Art & UI Components
# ══════════════════════════════════════════════════════════════

BANNER_3D = f"""
{C.FIRE_RED}{C.BOLD}
    ░██████╗██╗░░░██╗███╗░░██╗░█████╗░██████╗░████████╗██╗░█████╗░░██████╗
    ██╔════╝╚██╗░██╔╝████╗░██║██╔══██╗██╔══██╗╚══██╔══╝██║██╔══██╗██╔════╝
    ╚█████╗░░╚████╔╝░██╔██╗██║███████║██████╔╝░░░██║░░░██║██║░░╚═╝╚█████╗░
    ░╚═══██╗░░╚██╔╝░░██║╚████║██╔══██║██╔═══╝░░░░██║░░░██║██║░░██╗░╚═══██╗
    ██████╔╝░░░██║░░░██║░╚███║██║░░██║██║░░░░░░░░██║░░░██║╚█████╔╝██████╔╝
    ╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░░░░░░╚═╝░░░╚═╝░╚════╝░╚═════╝{C.RESET}

{C.CRIMSON}{C.BOLD}    ██╗░░██╗██╗██╗░░░░░██╗░░░░░███████╗██████╗░
    ██║░██╔╝██║██║░░░░░██║░░░░░██╔════╝██╔══██╗
    █████╔╝░██║██║░░░░░██║░░░░░█████╗░░██████╔╝
    ██╔═██╗░██║██║░░░░░██║░░░░░██╔══╝░░██╔══██╗
    ██║░╚██╗██║███████╗███████╗███████╗██║░░██║
    ╚═╝░░╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝░░╚═╝{C.RESET}
"""

SKULL_ART = f"""{C.DARK_RED}
                            ░░░░░░░░░░░░░░░░
                        ░░▒▒▓▓████████████▓▓▒▒░░
                      ░▒▓██████████████████████▓▒░
                    ░▒████████████████████████████▒░
                   ░▓██████████████████████████████▓░
                  ░████████████████████████████████████░
                  ▓█████████▓▓░░░░░░░░░░▓▓█████████████▓
                  ████████▓░░            ░░▓████████████
                  ███████░  ████████████░  ░███████████
                  ██████░  ██{C.WHITE}▓▓▓▓▓▓▓▓{C.DARK_RED}████  ░██████████
                  ██████░  ██{C.WHITE}▓▓▓▓▓▓▓▓{C.DARK_RED}████  ░██████████
                  ███████░  ████████████░  ░███████████
                  ████████▓░░            ░░▓████████████
                  ▓█████████▓▓░░░░░░░░░░▓▓█████████████▓
                  ░█████████████▓▓▓▓▓▓█████████████████░
                   ░▓████████  ░▓████▓░  ████████████▓░
                    ░▒████████▓▓██████▓▓████████████▒░
                      ░▒▓███████▓▓▓▓▓▓███████████▓▒░
                        ░░▒▒▓▓████████████▓▓▒▒░░
                            ░░░░░░░░░░░░░░░░{C.RESET}
"""


def print_separator(char="═", color=C.DARK_RED):
    w = get_terminal_width()
    print(f"{color}{char * w}{C.RESET}")


def print_box_line(text, color=C.CRIMSON, width=None):
    if width is None:
        width = get_terminal_width() - 4
    pad = width - len(text.replace('\033[', '').split('m', 1)[-1] if '\033[' in text else text)
    # Simple approach
    clean = ""
    i = 0
    raw = text
    while i < len(raw):
        if raw[i] == '\033':
            j = raw.find('m', i)
            if j != -1:
                i = j + 1
                continue
        clean += raw[i]
        i += 1
    pad = max(0, width - len(clean))
    print(f"  {color}║{C.RESET} {text}{' ' * pad} {color}║{C.RESET}")


def print_box_top(color=C.CRIMSON, width=None):
    if width is None:
        width = get_terminal_width() - 2
    print(f"  {color}╔{'═' * width}╗{C.RESET}")


def print_box_bottom(color=C.CRIMSON, width=None):
    if width is None:
        width = get_terminal_width() - 2
    print(f"  {color}╚{'═' * width}╝{C.RESET}")


def print_box_separator(color=C.CRIMSON, width=None):
    if width is None:
        width = get_terminal_width() - 2
    print(f"  {color}╠{'═' * width}╣{C.RESET}")


def animated_text(text, delay=0.015, color=C.WHITE):
    for ch in text:
        sys.stdout.write(f"{color}{ch}{C.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def progress_bar(current, total, prefix="", bar_length=40):
    fraction = current / total if total > 0 else 0
    filled = int(bar_length * fraction)
    bar_fill = "█" * filled
    bar_empty = "░" * (bar_length - filled)
    pct = fraction * 100

    # Color gradient based on progress
    if pct < 30:
        bar_color = C.DARK_RED
    elif pct < 60:
        bar_color = C.CRIMSON
    elif pct < 90:
        bar_color = C.FIRE_RED
    else:
        bar_color = C.GREEN

    sys.stdout.write(
        f"\r  {C.GRAY}{prefix} {bar_color}[{bar_fill}{C.DARK_GRAY}{bar_empty}{bar_color}]{C.RESET}"
        f" {C.WHITE}{C.BOLD}{pct:5.1f}%{C.RESET} "
        f"{C.GRAY}({current}/{total}){C.RESET}"
    )
    sys.stdout.flush()


def print_status(icon, message, color=C.WHITE):
    icons = {
        "ok":      f"{C.GREEN}  [✓]{C.RESET}",
        "fail":    f"{C.FIRE_RED}  [✗]{C.RESET}",
        "warn":    f"{C.YELLOW}  [!]{C.RESET}",
        "info":    f"{C.CYAN}  [i]{C.RESET}",
        "scan":    f"{C.CRIMSON}  [⊕]{C.RESET}",
        "kill":    f"{C.FIRE_RED}  [☠]{C.RESET}",
        "fix":     f"{C.GREEN}  [⚡]{C.RESET}",
        "file":    f"{C.SCARLET}  [📄]{C.RESET}",
        "shield":  f"{C.CRIMSON}  [🛡]{C.RESET}",
        "search":  f"{C.ORANGE_RED}  [🔍]{C.RESET}",
        "trash":   f"{C.FIRE_RED}  [🗑]{C.RESET}",
        "backup":  f"{C.YELLOW}  [💾]{C.RESET}",
        "rocket":  f"{C.SCARLET}  [🚀]{C.RESET}",
    }
    ico = icons.get(icon, f"  [{icon}]")
    print(f"{ico} {color}{message}{C.RESET}")


def type_effect(text, delay=0.02, color=C.RED):
    sys.stdout.write(f"  {color}")
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(f"{C.RESET}\n")


# ══════════════════════════════════════════════════════════════
#  PE File Parsing (Lightweight - No external dependencies)
# ══════════════════════════════════════════════════════════════

class PEParser:
    """Minimal PE parser to extract resources and version info from EXE files."""

    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None
        self.is_valid = False
        self.is_32bit = False
        self.sections = []
        self.resource_dir_rva = 0
        self.resource_dir_size = 0
        self.resource_section_offset = 0

    def load(self):
        try:
            with open(self.filepath, 'rb') as f:
                self.data = f.read()
            if len(self.data) < 64:
                return False
            # Check MZ header
            if self.data[0:2] != b'MZ':
                return False
            # Get PE header offset
            pe_offset = struct.unpack_from('<I', self.data, 0x3C)[0]
            if pe_offset + 4 > len(self.data):
                return False
            # Check PE signature
            if self.data[pe_offset:pe_offset + 4] != b'PE\x00\x00':
                return False
            # Machine type
            machine = struct.unpack_from('<H', self.data, pe_offset + 4)[0]
            self.is_32bit = (machine == 0x14C)  # IMAGE_FILE_MACHINE_I386
            self.is_valid = True
            self._parse_sections(pe_offset)
            return True
        except Exception:
            return False

    def _parse_sections(self, pe_offset):
        """Parse section headers to find resource section."""
        # COFF header fields
        num_sections = struct.unpack_from('<H', self.data, pe_offset + 6)[0]
        optional_header_size = struct.unpack_from('<H', self.data, pe_offset + 20)[0]

        # Optional header
        oh_offset = pe_offset + 24
        magic = struct.unpack_from('<H', self.data, oh_offset)[0]

        # Data directories offset
        if magic == 0x10B:  # PE32
            dd_offset = oh_offset + 96
        elif magic == 0x20B:  # PE32+
            dd_offset = oh_offset + 112
        else:
            return

        # Resource directory is the 3rd data directory entry (index 2)
        res_dd_offset = dd_offset + 2 * 8  # Each entry is 8 bytes
        if res_dd_offset + 8 <= len(self.data):
            self.resource_dir_rva = struct.unpack_from('<I', self.data, res_dd_offset)[0]
            self.resource_dir_size = struct.unpack_from('<I', self.data, res_dd_offset + 4)[0]

        # Parse sections
        section_offset = oh_offset + optional_header_size
        for i in range(num_sections):
            s_off = section_offset + i * 40
            if s_off + 40 > len(self.data):
                break
            name = self.data[s_off:s_off + 8].rstrip(b'\x00').decode('ascii', errors='ignore')
            virtual_size = struct.unpack_from('<I', self.data, s_off + 8)[0]
            virtual_addr = struct.unpack_from('<I', self.data, s_off + 12)[0]
            raw_size = struct.unpack_from('<I', self.data, s_off + 16)[0]
            raw_offset = struct.unpack_from('<I', self.data, s_off + 20)[0]
            self.sections.append({
                'name': name,
                'virtual_size': virtual_size,
                'virtual_addr': virtual_addr,
                'raw_size': raw_size,
                'raw_offset': raw_offset,
            })
            if self.resource_dir_rva != 0 and virtual_addr <= self.resource_dir_rva < virtual_addr + virtual_size:
                self.resource_section_offset = raw_offset - virtual_addr

    def rva_to_offset(self, rva):
        """Convert RVA to file offset."""
        for sec in self.sections:
            if sec['virtual_addr'] <= rva < sec['virtual_addr'] + sec['raw_size']:
                return rva - sec['virtual_addr'] + sec['raw_offset']
        return None

    def find_resource_by_name(self, name_target):
        """
        Search resource directory tree for a named resource (like 'EXERESX').
        Returns the raw data bytes if found, or None.
        """
        if self.resource_dir_rva == 0 or self.resource_section_offset == 0:
            return None

        base_offset = self.rva_to_offset(self.resource_dir_rva)
        if base_offset is None:
            return None

        try:
            return self._search_resource_tree(base_offset, base_offset, name_target, depth=0)
        except Exception:
            return None

    def _search_resource_tree(self, base, dir_offset, name_target, depth):
        """Recursively search resource directory tree."""
        if depth > 3 or dir_offset + 16 > len(self.data):
            return None

        num_named = struct.unpack_from('<H', self.data, dir_offset + 12)[0]
        num_id = struct.unpack_from('<H', self.data, dir_offset + 14)[0]
        total = num_named + num_id

        entry_offset = dir_offset + 16
        for i in range(total):
            if entry_offset + 8 > len(self.data):
                break
            name_or_id = struct.unpack_from('<I', self.data, entry_offset)[0]
            data_or_subdir = struct.unpack_from('<I', self.data, entry_offset + 4)[0]

            # Check if this is a named entry
            entry_name = None
            if name_or_id & 0x80000000:
                name_offset = base + (name_or_id & 0x7FFFFFFF)
                if name_offset + 2 < len(self.data):
                    name_len = struct.unpack_from('<H', self.data, name_offset)[0]
                    if name_offset + 2 + name_len * 2 <= len(self.data):
                        raw_name = self.data[name_offset + 2:name_offset + 2 + name_len * 2]
                        try:
                            entry_name = raw_name.decode('utf-16-le')
                        except Exception:
                            entry_name = None

            # If subdirectory
            if data_or_subdir & 0x80000000:
                subdir_off = base + (data_or_subdir & 0x7FFFFFFF)
                result = self._search_resource_tree(base, subdir_off, name_target, depth + 1)
                if result is not None:
                    # Check if the name matches at the right depth
                    if entry_name and entry_name.upper() == name_target.upper():
                        return result
                    elif depth > 0:
                        return result
            else:
                # Data entry
                data_entry_offset = base + data_or_subdir
                if data_entry_offset + 16 <= len(self.data):
                    data_rva = struct.unpack_from('<I', self.data, data_entry_offset)[0]
                    data_size = struct.unpack_from('<I', self.data, data_entry_offset + 4)[0]
                    file_offset = self.rva_to_offset(data_rva)
                    if file_offset is not None and file_offset + data_size <= len(self.data):
                        if entry_name and entry_name.upper() == name_target.upper():
                            return self.data[file_offset:file_offset + data_size]

            entry_offset += 8
        return None

    def get_version_info_string(self, target_string="FileDescription"):
        """Extract a string from version info resource."""
        try:
            # Search for the target string in the binary data as UTF-16LE
            search_bytes = target_string.encode('utf-16-le')
            idx = self.data.find(search_bytes)
            if idx == -1:
                return None

            # The value follows the key in version info structures
            # Skip past the key and padding
            key_end = idx + len(search_bytes) + 2  # +2 for null terminator
            # Align to DWORD boundary
            key_end = (key_end + 3) & ~3

            # Read the value (UTF-16LE string)
            value_bytes = bytearray()
            pos = key_end
            while pos + 1 < len(self.data):
                ch = struct.unpack_from('<H', self.data, pos)[0]
                if ch == 0:
                    break
                value_bytes.extend(struct.pack('<H', ch))
                pos += 2

            if value_bytes:
                return value_bytes.decode('utf-16-le', errors='ignore')
            return None
        except Exception:
            return None


def check_exe_infected(filepath):
    """
    Check if an EXE file is infected by Synaptics virus.
    Returns (is_infected: bool, pe: PEParser or None)
    """
    try:
        pe = PEParser(filepath)
        if not pe.load():
            return False, None

        # Check if it's 32-bit (virus only infects 32-bit executables)
        if not pe.is_32bit:
            return False, None

        # Check FileDescription for "Synaptics Pointing Device Driver"
        desc = pe.get_version_info_string("FileDescription")
        if desc and "Synaptics Pointing Device Driver" in desc:
            return True, pe

        # Also check for EXERESX resource (infected files contain original in this resource)
        # Search for the marker in binary
        if b'EXERESX' in pe.data:
            desc2 = pe.get_version_info_string("FileDescription")
            if desc2 and "Synaptics" in desc2:
                return True, pe

        return False, pe
    except Exception:
        return False, None


def extract_original_exe(filepath, pe):
    """
    Extract the original EXE from EXERESX resource of an infected file.
    Returns the original file data or None.
    """
    try:
        # Try to find EXERESX resource
        exeresx_data = pe.find_resource_by_name("EXERESX")
        if exeresx_data and len(exeresx_data) > 0:
            # Verify it starts with MZ
            if exeresx_data[:2] == b'MZ':
                return exeresx_data

        # Alternative: Search for embedded PE after the virus code
        # The virus prepends itself to the original EXE
        # Look for second MZ header
        data = pe.data
        second_mz = data.find(b'MZ', 1)
        while second_mz != -1:
            # Verify this is a valid PE
            if second_mz + 0x3C + 4 < len(data):
                pe_off = struct.unpack_from('<I', data, second_mz + 0x3C)[0]
                if second_mz + pe_off + 4 < len(data):
                    if data[second_mz + pe_off:second_mz + pe_off + 4] == b'PE\x00\x00':
                        return data[second_mz:]
            second_mz = data.find(b'MZ', second_mz + 1)

        return None
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════
#  XLSX/XLSM Recovery
# ══════════════════════════════════════════════════════════════

def check_xlsm_infected(filepath):
    """
    Check if an XLSM file is infected by Synaptics virus.
    The virus injects VBA macros containing malicious URLs.
    """
    try:
        if not zipfile.is_zipfile(filepath):
            return False

        with zipfile.ZipFile(filepath, 'r') as zf:
            names = zf.namelist()
            # Check for VBA project
            if 'xl/vbaProject.bin' not in names:
                return False

            # Read the VBA binary and check for known virus signatures
            vba_data = zf.read('xl/vbaProject.bin')

            # Known Synaptics/XRed indicators in VBA
            virus_signatures = [
                b'xred.mooo.com',
                b'Synaptics',
                b'freedns.afraid.org',
                b'xred.site50.net',
                b'xredline1@gmail.com',
                b'SUpdate.ini',
                b'Synaptics Pointing Device Driver',
                b'ProgramData\\Synaptics',
            ]

            for sig in virus_signatures:
                if sig.lower() in vba_data.lower():
                    return True

        return False
    except Exception:
        return False


def recover_xlsm_to_xlsx(src_path, dst_path):
    """
    Recover infected XLSM by removing VBA macros and saving as XLSX.
    """
    try:
        # Files to exclude (VBA/macro related)
        exclude_files = {
            'xl/vbaProject.bin',
            'xl/vbaData.xml',
        }

        with zipfile.ZipFile(src_path, 'r') as zin:
            with zipfile.ZipFile(dst_path, 'w', zipfile.ZIP_DEFLATED) as zout:
                for item in zin.namelist():
                    # Skip VBA related files
                    if item in exclude_files:
                        continue
                    # Skip if it references VBA
                    if 'vba' in item.lower() and item.endswith('.bin'):
                        continue

                    data = zin.read(item)

                    # Fix content types to remove macro references
                    if item == '[Content_Types].xml':
                        data = data.replace(
                            b'application/vnd.ms-excel.sheet.macroEnabled.main+xml',
                            b'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml'
                        )
                        # Remove vbaProject content type entry
                        lines = data.split(b'\n')
                        cleaned = []
                        for line in lines:
                            if b'vbaProject' not in line and b'vbaData' not in line:
                                cleaned.append(line)
                        data = b'\n'.join(cleaned)

                    # Fix workbook.xml.rels to remove VBA reference
                    if item == 'xl/_rels/workbook.xml.rels':
                        lines = data.split(b'\n')
                        cleaned = []
                        for line in lines:
                            if b'vbaProject' not in line:
                                cleaned.append(line)
                        data = b'\n'.join(cleaned)

                    zout.writestr(item, data)
        return True
    except Exception as e:
        return False


# ══════════════════════════════════════════════════════════════
#  System Cleanup (Process Kill, Registry, Virus Files)
# ══════════════════════════════════════════════════════════════

def is_admin():
    """Check if running as administrator."""
    if os.name == 'nt':
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    return os.geteuid() == 0 if hasattr(os, 'geteuid') else False


def kill_virus_processes():
    """Kill Synaptics.exe and infected EXCEL.EXE processes."""
    killed = []
    target_processes = ['Synaptics.exe', 'EXCEL.EXE']

    if os.name == 'nt':
        for proc_name in target_processes:
            try:
                result = subprocess.run(
                    ['taskkill', '/F', '/IM', proc_name],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    killed.append(proc_name)
            except Exception:
                pass
    else:
        # Linux/Mac - for testing purposes
        for proc_name in target_processes:
            try:
                result = subprocess.run(
                    ['pkill', '-f', proc_name],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    killed.append(proc_name)
            except Exception:
                pass
    return killed


def clean_registry():
    """Remove Synaptics virus registry entries."""
    cleaned = []
    if os.name != 'nt':
        return cleaned

    try:
        import winreg
        # Registry paths used by the virus
        reg_paths = [
            (winreg.HKEY_LOCAL_MACHINE,
             r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run",
             "Synaptics Pointing Device Driver"),
            (winreg.HKEY_LOCAL_MACHINE,
             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
             "Synaptics Pointing Device Driver"),
            (winreg.HKEY_CURRENT_USER,
             r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
             "Synaptics Pointing Device Driver"),
        ]

        for hive, path, value_name in reg_paths:
            try:
                key = winreg.OpenKey(hive, path, 0, winreg.KEY_ALL_ACCESS)
                try:
                    val, _ = winreg.QueryValueEx(key, value_name)
                    if 'Synaptics' in val:
                        winreg.DeleteValue(key, value_name)
                        cleaned.append(f"{path}\\{value_name}")
                except FileNotFoundError:
                    pass
                finally:
                    winreg.CloseKey(key)
            except Exception:
                pass
    except ImportError:
        pass

    return cleaned


def delete_virus_files():
    """Delete Synaptics virus files from ProgramData."""
    deleted = []
    virus_dirs = []

    if os.name == 'nt':
        virus_dirs = [
            os.path.join(os.environ.get('ALLUSERSPROFILE', 'C:\\ProgramData'), 'Synaptics'),
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32', 'Synaptics'),
        ]
    
    for vdir in virus_dirs:
        if os.path.isdir(vdir):
            try:
                shutil.rmtree(vdir)
                deleted.append(vdir)
            except Exception:
                # Try individual files
                for f in os.listdir(vdir):
                    fp = os.path.join(vdir, f)
                    try:
                        os.remove(fp)
                        deleted.append(fp)
                    except Exception:
                        pass
    return deleted


# ══════════════════════════════════════════════════════════════
#  Scanner & Recovery Engine
# ══════════════════════════════════════════════════════════════

class ScanResult:
    def __init__(self):
        self.infected_exe = []
        self.infected_xlsm = []
        self.recovered_exe = []
        self.recovered_xlsx = []
        self.failed = []
        self.total_scanned = 0
        self.scan_time = 0


def get_scan_directories():
    """Get default directories to scan."""
    dirs = []
    if os.name == 'nt':
        user_profile = os.environ.get('USERPROFILE', '')
        for folder in ['Downloads', 'Documents', 'Desktop']:
            path = os.path.join(user_profile, folder)
            if os.path.isdir(path):
                dirs.append(path)
    else:
        home = os.path.expanduser('~')
        for folder in ['Downloads', 'Documents', 'Desktop']:
            path = os.path.join(home, folder)
            if os.path.isdir(path):
                dirs.append(path)
    return dirs


def scan_directory(directory, create_backup=True, callback=None):
    """
    Scan a directory recursively for infected files.
    Returns ScanResult.
    """
    result = ScanResult()
    start_time = time.time()

    # Collect all target files first
    all_files = []
    for root, dirs, files in os.walk(directory):
        # Skip system directories
        skip_dirs = ['.git', '__pycache__', 'node_modules', '.venv', 'venv']
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for f in files:
            ext = f.lower().split('.')[-1] if '.' in f else ''
            if ext in ('exe', 'xlsm'):
                all_files.append(os.path.join(root, f))

    total = len(all_files)

    for idx, filepath in enumerate(all_files):
        result.total_scanned += 1

        if callback:
            callback(idx + 1, total, filepath)

        ext = filepath.lower().split('.')[-1]

        try:
            if ext == 'exe':
                infected, pe = check_exe_infected(filepath)
                if infected:
                    result.infected_exe.append(filepath)

                    # Try to extract original
                    original_data = extract_original_exe(filepath, pe)
                    if original_data:
                        if create_backup:
                            backup_path = filepath + '.bak'
                            shutil.copy2(filepath, backup_path)

                        # Write recovered file
                        with open(filepath, 'wb') as f:
                            f.write(original_data)
                        result.recovered_exe.append(filepath)
                    else:
                        result.failed.append((filepath, "Could not extract original EXE"))

            elif ext == 'xlsm':
                if check_xlsm_infected(filepath):
                    result.infected_xlsm.append(filepath)

                    # Recover to XLSX
                    xlsx_path = filepath[:-5] + '.xlsx'  # .xlsm -> .xlsx
                    success = recover_xlsm_to_xlsx(filepath, xlsx_path)

                    if success:
                        if create_backup:
                            backup_path = filepath + '.bak'
                            os.rename(filepath, backup_path)
                        else:
                            os.remove(filepath)
                        result.recovered_xlsx.append(xlsx_path)
                    else:
                        result.failed.append((filepath, "Failed to remove macros"))

        except Exception as e:
            result.failed.append((filepath, str(e)))

    result.scan_time = time.time() - start_time
    return result


# ══════════════════════════════════════════════════════════════
#  Report Generator
# ══════════════════════════════════════════════════════════════

def generate_report(result, output_dir=None):
    """Generate a recovery report."""
    if output_dir is None:
        output_dir = os.path.expanduser('~')

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = os.path.join(output_dir, f'SynapticsKiller_Report_{timestamp}.txt')

    lines = []
    lines.append("=" * 70)
    lines.append("  SYNAPTICS-KILLER RECOVERY REPORT")
    lines.append(f"  Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"  Set By AlexDev | v2.0")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"  Total Files Scanned    : {result.total_scanned}")
    lines.append(f"  Infected EXE Found     : {len(result.infected_exe)}")
    lines.append(f"  Infected XLSM Found    : {len(result.infected_xlsm)}")
    lines.append(f"  Successfully Recovered : {len(result.recovered_exe) + len(result.recovered_xlsx)}")
    lines.append(f"  Failed                 : {len(result.failed)}")
    lines.append(f"  Scan Duration          : {result.scan_time:.2f}s")
    lines.append("")

    if result.recovered_exe:
        lines.append("-" * 70)
        lines.append("  RECOVERED EXE FILES:")
        lines.append("-" * 70)
        for f in result.recovered_exe:
            lines.append(f"    [OK] {f}")
        lines.append("")

    if result.recovered_xlsx:
        lines.append("-" * 70)
        lines.append("  RECOVERED XLSX FILES:")
        lines.append("-" * 70)
        for f in result.recovered_xlsx:
            lines.append(f"    [OK] {f}")
        lines.append("")

    if result.failed:
        lines.append("-" * 70)
        lines.append("  FAILED:")
        lines.append("-" * 70)
        for f, reason in result.failed:
            lines.append(f"    [FAIL] {f}")
            lines.append(f"           Reason: {reason}")
        lines.append("")

    lines.append("=" * 70)
    lines.append("  END OF REPORT")
    lines.append("=" * 70)

    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return report_path
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════
#  Main UI / Menu System
# ══════════════════════════════════════════════════════════════

def show_header():
    """Display the main header with 3D ASCII art."""
    clear_screen()
    print(BANNER_3D)

    w = get_terminal_width()
    tagline = "⚔  XRed Backdoor Recovery Tool  ⚔"
    credit  = "Set By AlexDev  |  v2.0  |  GPL-3.0"

    print(f"{C.BOLD}{C.WHITE}{'─' * w}{C.RESET}")
    print(f"{C.BOLD}{C.FIRE_RED}{tagline:^{w}}{C.RESET}")
    print(f"{C.DIM}{C.LIGHT_GRAY}{credit:^{w}}{C.RESET}")
    print(f"{C.BOLD}{C.WHITE}{'─' * w}{C.RESET}")
    print()


def show_system_info():
    """Display system information panel."""
    print()
    print_box_top()
    print_box_line(f"{C.FIRE_RED}{C.BOLD}  ◆  SYSTEM INFORMATION{C.RESET}")
    print_box_separator()

    import platform
    os_name = platform.system()
    os_ver = platform.version()
    hostname = platform.node()
    arch = platform.architecture()[0]
    py_ver = platform.python_version()
    admin_status = f"{C.GREEN}Yes ✓{C.RESET}" if is_admin() else f"{C.YELLOW}No (Limited){C.RESET}"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print_box_line(f"  {C.GRAY}OS          :{C.RESET} {C.WHITE}{os_name} {os_ver}{C.RESET}")
    print_box_line(f"  {C.GRAY}Hostname    :{C.RESET} {C.WHITE}{hostname}{C.RESET}")
    print_box_line(f"  {C.GRAY}Architecture:{C.RESET} {C.WHITE}{arch}{C.RESET}")
    print_box_line(f"  {C.GRAY}Python      :{C.RESET} {C.WHITE}{py_ver}{C.RESET}")
    print_box_line(f"  {C.GRAY}Admin       :{C.RESET} {admin_status}")
    print_box_line(f"  {C.GRAY}Date/Time   :{C.RESET} {C.WHITE}{now}{C.RESET}")
    print_box_bottom()
    print()


def show_main_menu():
    """Display the main menu."""
    print()
    print_box_top()
    print_box_line(f"{C.FIRE_RED}{C.BOLD}  ◆  MAIN MENU{C.RESET}")
    print_box_separator()
    print_box_line(f"")
    print_box_line(f"  {C.FIRE_RED}{C.BOLD}[1]{C.RESET} {C.WHITE}🔥 Scan & Recover {C.GRAY}(without .bak backup){C.RESET}")
    print_box_line(f"      {C.DIM}{C.LIGHT_GRAY}Overwrite infected files directly with recovered originals{C.RESET}")
    print_box_line(f"")
    print_box_line(f"  {C.CRIMSON}{C.BOLD}[2]{C.RESET} {C.WHITE}💾 Scan & Recover {C.GRAY}(with .bak backup){C.RESET}")
    print_box_line(f"      {C.DIM}{C.LIGHT_GRAY}Create backup before recovery for safety{C.RESET}")
    print_box_line(f"")
    print_box_line(f"  {C.SCARLET}{C.BOLD}[3]{C.RESET} {C.WHITE}☠  Kill Virus Processes & Clean System{C.RESET}")
    print_box_line(f"      {C.DIM}{C.LIGHT_GRAY}Terminate Synaptics.exe, clean registry & virus files{C.RESET}")
    print_box_line(f"")
    print_box_line(f"  {C.ORANGE_RED}{C.BOLD}[4]{C.RESET} {C.WHITE}🔍 Scan Only {C.GRAY}(detect without recovery){C.RESET}")
    print_box_line(f"      {C.DIM}{C.LIGHT_GRAY}Find infected files without making any changes{C.RESET}")
    print_box_line(f"")
    print_box_line(f"  {C.DARK_RED}{C.BOLD}[5]{C.RESET} {C.WHITE}📂 Custom Directory Scan{C.RESET}")
    print_box_line(f"      {C.DIM}{C.LIGHT_GRAY}Specify a custom directory path to scan{C.RESET}")
    print_box_line(f"")
    print_box_line(f"  {C.GRAY}{C.BOLD}[0]{C.RESET} {C.GRAY}Exit{C.RESET}")
    print_box_line(f"")
    print_box_bottom()
    print()


def show_loading_animation(text="Initializing", duration=1.5):
    """Show a loading animation."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r  {C.FIRE_RED}{frames[i % len(frames)]}{C.RESET} {C.WHITE}{text}...{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write(f"\r  {C.GREEN}✓{C.RESET} {C.WHITE}{text} Complete{C.RESET}           \n")


def run_scan_and_recover(create_backup, custom_dir=None):
    """Execute scan and recovery operation."""
    print()
    print_separator("▓", C.FIRE_RED)
    print(f"  {C.BOLD}{C.FIRE_RED}⚡ SCAN & RECOVERY ENGINE ⚡{C.RESET}")
    print_separator("▓", C.FIRE_RED)
    print()

    # Determine scan directories
    if custom_dir:
        scan_dirs = [custom_dir]
    else:
        scan_dirs = get_scan_directories()

    if not scan_dirs:
        print_status("warn", "No directories found to scan!")
        return

    # Display scan targets
    print_status("info", f"Backup mode: {C.BOLD}{'Enabled (.bak)' if create_backup else 'Disabled (overwrite)'}{C.RESET}")
    print_status("info", f"Scan targets:")
    for d in scan_dirs:
        print(f"      {C.GRAY}└─ {C.WHITE}{d}{C.RESET}")
    print()

    show_loading_animation("Preparing scan engine")
    print()

    # Scan each directory
    total_result = ScanResult()

    for scan_dir in scan_dirs:
        print(f"  {C.CRIMSON}{'━' * 50}{C.RESET}")
        print_status("search", f"Scanning: {C.BOLD}{scan_dir}{C.RESET}")
        print(f"  {C.CRIMSON}{'━' * 50}{C.RESET}")

        def scan_callback(current, total, filepath):
            fname = os.path.basename(filepath)
            if len(fname) > 30:
                fname = fname[:27] + "..."
            progress_bar(current, total, f"  {fname:<32}")

        result = scan_directory(scan_dir, create_backup, scan_callback)

        # Merge results
        total_result.infected_exe.extend(result.infected_exe)
        total_result.infected_xlsm.extend(result.infected_xlsm)
        total_result.recovered_exe.extend(result.recovered_exe)
        total_result.recovered_xlsx.extend(result.recovered_xlsx)
        total_result.failed.extend(result.failed)
        total_result.total_scanned += result.total_scanned
        total_result.scan_time += result.scan_time

        print()  # New line after progress bar
        print()

    # Show results
    show_scan_results(total_result)

    # Generate report
    report_path = generate_report(total_result)
    if report_path:
        print_status("ok", f"Report saved: {C.UNDERLINE}{report_path}{C.RESET}")

    print()


def run_scan_only(custom_dir=None):
    """Scan only without recovery."""
    print()
    print_separator("▓", C.CRIMSON)
    print(f"  {C.BOLD}{C.CRIMSON}🔍 DETECTION SCAN (Read-Only) 🔍{C.RESET}")
    print_separator("▓", C.CRIMSON)
    print()

    if custom_dir:
        scan_dirs = [custom_dir]
    else:
        scan_dirs = get_scan_directories()

    if not scan_dirs:
        print_status("warn", "No directories found to scan!")
        return

    show_loading_animation("Initializing scanner")
    print()

    total_infected_exe = []
    total_infected_xlsm = []
    total_scanned = 0

    for scan_dir in scan_dirs:
        print_status("search", f"Scanning: {C.BOLD}{scan_dir}{C.RESET}")

        for root, dirs, files in os.walk(scan_dir):
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules']]
            for f in files:
                filepath = os.path.join(root, f)
                ext = f.lower().split('.')[-1] if '.' in f else ''

                if ext == 'exe':
                    total_scanned += 1
                    infected, _ = check_exe_infected(filepath)
                    if infected:
                        total_infected_exe.append(filepath)
                        print_status("fail", f"INFECTED EXE: {C.FIRE_RED}{filepath}{C.RESET}")

                elif ext == 'xlsm':
                    total_scanned += 1
                    if check_xlsm_infected(filepath):
                        total_infected_xlsm.append(filepath)
                        print_status("fail", f"INFECTED XLSM: {C.FIRE_RED}{filepath}{C.RESET}")

    print()
    print_box_top()
    print_box_line(f"{C.BOLD}{C.FIRE_RED}  SCAN RESULTS{C.RESET}")
    print_box_separator()
    print_box_line(f"  {C.GRAY}Files Scanned    :{C.RESET} {C.WHITE}{total_scanned}{C.RESET}")
    print_box_line(f"  {C.GRAY}Infected EXE     :{C.RESET} {C.FIRE_RED if total_infected_exe else C.GREEN}{len(total_infected_exe)}{C.RESET}")
    print_box_line(f"  {C.GRAY}Infected XLSM    :{C.RESET} {C.FIRE_RED if total_infected_xlsm else C.GREEN}{len(total_infected_xlsm)}{C.RESET}")
    print_box_bottom()
    print()

    if not total_infected_exe and not total_infected_xlsm:
        print_status("shield", f"{C.GREEN}{C.BOLD}System appears clean! No infections detected.{C.RESET}")
    else:
        print_status("warn", f"{C.YELLOW}Infections found! Use option [1] or [2] to recover.{C.RESET}")
    print()


def show_scan_results(result):
    """Display formatted scan results."""
    print()
    print_box_top()
    print_box_line(f"{C.BOLD}{C.FIRE_RED}  ◆  RECOVERY RESULTS{C.RESET}")
    print_box_separator()
    print_box_line(f"  {C.GRAY}Total Scanned        :{C.RESET} {C.WHITE}{C.BOLD}{result.total_scanned}{C.RESET}")
    print_box_line(f"  {C.GRAY}Infected EXE Found   :{C.RESET} {C.FIRE_RED}{len(result.infected_exe)}{C.RESET}")
    print_box_line(f"  {C.GRAY}Infected XLSM Found  :{C.RESET} {C.FIRE_RED}{len(result.infected_xlsm)}{C.RESET}")
    print_box_separator()
    print_box_line(f"  {C.GRAY}Recovered EXE        :{C.RESET} {C.GREEN}{len(result.recovered_exe)}{C.RESET}")
    print_box_line(f"  {C.GRAY}Recovered XLSX       :{C.RESET} {C.GREEN}{len(result.recovered_xlsx)}{C.RESET}")
    print_box_line(f"  {C.GRAY}Failed               :{C.RESET} {C.FIRE_RED if result.failed else C.GREEN}{len(result.failed)}{C.RESET}")
    print_box_separator()
    print_box_line(f"  {C.GRAY}Duration             :{C.RESET} {C.WHITE}{result.scan_time:.2f}s{C.RESET}")
    print_box_bottom()
    print()

    # Detail recovered files
    if result.recovered_exe:
        print_status("ok", f"{C.GREEN}Recovered EXE files:{C.RESET}")
        for f in result.recovered_exe:
            print(f"      {C.GREEN}└─ ✓{C.RESET} {C.WHITE}{f}{C.RESET}")
        print()

    if result.recovered_xlsx:
        print_status("ok", f"{C.GREEN}Recovered XLSX files:{C.RESET}")
        for f in result.recovered_xlsx:
            print(f"      {C.GREEN}└─ ✓{C.RESET} {C.WHITE}{f}{C.RESET}")
        print()

    if result.failed:
        print_status("fail", f"{C.FIRE_RED}Failed recoveries:{C.RESET}")
        for f, reason in result.failed:
            print(f"      {C.FIRE_RED}└─ ✗{C.RESET} {C.WHITE}{f}{C.RESET}")
            print(f"        {C.GRAY}{reason}{C.RESET}")
        print()

    total_recovered = len(result.recovered_exe) + len(result.recovered_xlsx)
    total_infected = len(result.infected_exe) + len(result.infected_xlsm)

    if total_infected == 0:
        print_status("shield", f"{C.GREEN}{C.BOLD}✨ System appears clean! No infections detected. ✨{C.RESET}")
    elif total_recovered == total_infected:
        print_status("shield", f"{C.GREEN}{C.BOLD}✨ All infected files successfully recovered! ✨{C.RESET}")
    else:
        print_status("warn", f"{C.YELLOW}Some files could not be recovered. Check report for details.{C.RESET}")


def run_system_cleanup():
    """Kill virus processes and clean system."""
    print()
    print_separator("▓", C.FIRE_RED)
    print(f"  {C.BOLD}{C.FIRE_RED}☠  SYSTEM CLEANUP ENGINE  ☠{C.RESET}")
    print_separator("▓", C.FIRE_RED)
    print()

    if not is_admin():
        print_status("warn", f"{C.YELLOW}Running without admin privileges. Some operations may fail.{C.RESET}")
        print_status("info", "For full cleanup, run as Administrator.")
        print()

    # Step 1: Kill processes
    print(f"  {C.CRIMSON}{'━' * 50}{C.RESET}")
    print(f"  {C.BOLD}{C.WHITE}PHASE 1: Terminating Malicious Processes{C.RESET}")
    print(f"  {C.CRIMSON}{'━' * 50}{C.RESET}")
    show_loading_animation("Scanning processes")

    killed = kill_virus_processes()
    if killed:
        for proc in killed:
            print_status("kill", f"Terminated: {C.FIRE_RED}{C.BOLD}{proc}{C.RESET}")
    else:
        print_status("ok", f"{C.GREEN}No malicious processes found running.{C.RESET}")
    print()

    # Step 2: Clean registry
    print(f"  {C.CRIMSON}{'━' * 50}{C.RESET}")
    print(f"  {C.BOLD}{C.WHITE}PHASE 2: Cleaning Registry Entries{C.RESET}")
    print(f"  {C.CRIMSON}{'━' * 50}{C.RESET}")
    show_loading_animation("Scanning registry")

    cleaned_reg = clean_registry()
    if cleaned_reg:
        for entry in cleaned_reg:
            print_status("ok", f"Removed: {C.WHITE}{entry}{C.RESET}")
    else:
        print_status("ok", f"{C.GREEN}No virus registry entries found.{C.RESET}")
    print()

    # Step 3: Delete virus files
    print(f"  {C.CRIMSON}{'━' * 50}{C.RESET}")
    print(f"  {C.BOLD}{C.WHITE}PHASE 3: Removing Virus Files{C.RESET}")
    print(f"  {C.CRIMSON}{'━' * 50}{C.RESET}")
    show_loading_animation("Scanning filesystem")

    deleted = delete_virus_files()
    if deleted:
        for f in deleted:
            print_status("trash", f"Deleted: {C.FIRE_RED}{f}{C.RESET}")
    else:
        print_status("ok", f"{C.GREEN}No virus files found in system directories.{C.RESET}")

    print()
    print_box_top()
    print_box_line(f"{C.BOLD}{C.GREEN}  ◆  CLEANUP COMPLETE{C.RESET}")
    print_box_separator()
    print_box_line(f"  {C.GRAY}Processes Killed  :{C.RESET} {C.WHITE}{len(killed)}{C.RESET}")
    print_box_line(f"  {C.GRAY}Registry Cleaned  :{C.RESET} {C.WHITE}{len(cleaned_reg)}{C.RESET}")
    print_box_line(f"  {C.GRAY}Files Deleted     :{C.RESET} {C.WHITE}{len(deleted)}{C.RESET}")
    print_box_bottom()
    print()


def show_exit_screen():
    """Show exit animation and message."""
    print()
    exit_art = f"""
{C.DARK_RED}    ┌──────────────────────────────────────────────────────┐
    │                                                      │
    │   {C.FIRE_RED}{C.BOLD}Thank you for using Synaptics-Killer v2.0{C.DARK_RED}         │
    │   {C.LIGHT_GRAY}Set By AlexDev  •  Stay Safe  •  GPL-3.0{C.DARK_RED}          │
    │                                                      │
    │   {C.CRIMSON}╔═══╗                                           {C.DARK_RED}│
    │   {C.CRIMSON}║{C.FIRE_RED}►{C.CRIMSON}►{C.FIRE_RED}►{C.CRIMSON}║  {C.WHITE}github.com/AlexDev/Synaptics-Killer{C.DARK_RED}    │
    │   {C.CRIMSON}╚═══╝                                           {C.DARK_RED}│
    │                                                      │
    └──────────────────────────────────────────────────────┘{C.RESET}
"""
    print(exit_art)
    type_effect("  Shutting down... Goodbye! 👋", delay=0.03, color=C.DARK_RED)
    print()


# ══════════════════════════════════════════════════════════════
#  Main Application Loop
# ══════════════════════════════════════════════════════════════

def main():
    enable_ansi_windows()

    # Intro sequence
    clear_screen()
    show_loading_animation("Loading Synaptics-Killer", 1.0)
    show_loading_animation("Checking system configuration", 0.8)
    show_loading_animation("Initializing recovery modules", 0.6)
    time.sleep(0.3)

    while True:
        show_header()
        show_system_info()
        show_main_menu()

        try:
            choice = input(f"  {C.FIRE_RED}❯{C.RESET} {C.BOLD}{C.WHITE}Select option{C.RESET} {C.GRAY}[0-5]{C.RESET}: ").strip()
        except (KeyboardInterrupt, EOFError):
            show_exit_screen()
            break

        if choice == '1':
            # Scan & Recover without backup
            run_scan_and_recover(create_backup=False)
            input(f"\n  {C.GRAY}Press Enter to return to menu...{C.RESET}")

        elif choice == '2':
            # Scan & Recover with backup
            run_scan_and_recover(create_backup=True)
            input(f"\n  {C.GRAY}Press Enter to return to menu...{C.RESET}")

        elif choice == '3':
            # System cleanup
            print()
            print_status("warn", f"{C.YELLOW}This will kill virus processes and clean system entries.{C.RESET}")
            confirm = input(f"  {C.FIRE_RED}❯{C.RESET} {C.WHITE}Continue? {C.GRAY}[y/N]{C.RESET}: ").strip().lower()
            if confirm in ('y', 'yes'):
                run_system_cleanup()
            else:
                print_status("info", "Operation cancelled.")
            input(f"\n  {C.GRAY}Press Enter to return to menu...{C.RESET}")

        elif choice == '4':
            # Scan only
            run_scan_only()
            input(f"\n  {C.GRAY}Press Enter to return to menu...{C.RESET}")

        elif choice == '5':
            # Custom directory scan
            print()
            custom_path = input(f"  {C.FIRE_RED}❯{C.RESET} {C.WHITE}Enter directory path: {C.RESET}").strip()
            if custom_path and os.path.isdir(custom_path):
                print()
                print_status("info", f"Backup mode?")
                bk = input(f"  {C.FIRE_RED}❯{C.RESET} {C.WHITE}Create .bak backups? {C.GRAY}[y/N]{C.RESET}: ").strip().lower()
                create_bk = bk in ('y', 'yes')
                run_scan_and_recover(create_backup=create_bk, custom_dir=custom_path)
            elif custom_path:
                print_status("fail", f"Directory not found: {custom_path}")
            input(f"\n  {C.GRAY}Press Enter to return to menu...{C.RESET}")

        elif choice == '0':
            show_exit_screen()
            break

        else:
            print_status("warn", f"{C.YELLOW}Invalid option. Please select 0-5.{C.RESET}")
            time.sleep(1)


if __name__ == '__main__':
    main()