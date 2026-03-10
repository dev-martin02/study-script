"""
Setup autostart for the file watching script.
This script adds main.py to Windows autostart registry.
Run this once to enable autostart.
"""

import winreg
from pathlib import Path

# Get the path to the virtual environment Python executable
venv_python = Path.home() / "OneDrive" / "Desktop" / "study-script" / ".venv" / "Scripts" / "python.exe"
script_path = Path.home() / "OneDrive" / "Desktop" / "study-script" / "main.py"

# Create batch file to run main.py with venv
batch_file = Path.home() / "OneDrive" / "Desktop" / "study-script" / "run_main.bat"
batch_content = f"""@echo off
cd /d "{Path.home() / 'OneDrive' / 'Desktop' / 'study-script'}"
"{venv_python}" "{script_path}"
pause
"""

# Write batch file
batch_file.write_text(batch_content)
print(f"✓ Created batch file: {batch_file}")

# Add to Windows autostart registry
registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
value_name = "StudyScript"

try:
    # Open registry key (create if doesn't exist)
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE) as key:
        # Set the value to point to the batch file
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, str(batch_file))
    
    print(f"✓ Added '{value_name}' to Windows autostart")
    print(f"✓ Registry Entry: HKEY_CURRENT_USER\\{registry_path}\\{value_name}")
    print(f"✓ Value: {batch_file}")
    print("\n✓ Setup complete! The script will run automatically on next login.")
    
except PermissionError:
    print("❌ Permission denied. Run this script as Administrator.")
except Exception as e:
    print(f"❌ Error: {e}")


# Optional: Function to remove from autostart
def remove_autostart():
    """Remove the script from autostart."""
    registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value_name = "StudyScript"
    
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE) as key:
            winreg.DeleteValue(key, value_name)
        print(f"✓ Removed '{value_name}' from Windows autostart")
    except FileNotFoundError:
        print(f"❌ Registry entry not found")
    except PermissionError:
        print("❌ Permission denied. Run as Administrator.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "remove":
        remove_autostart()
