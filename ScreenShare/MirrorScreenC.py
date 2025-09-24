import subprocess
import os

def run_command(cmd):
    """Pokreni komandu i vrati (kod, izlaz, error)."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def main():
    print("🔌 Diskonektiram sve TCP/IP veze...")
    run_command(["adb", "disconnect"])

    print("🔍 Provjeravam uređaje...")
    code, out, err = run_command(["adb", "devices"])
    if code != 0:
        print("❌ Greška kod provjere uređaja:", err or out)
        os.system("pause")
        return

    # Parsiraj listu uređaja
    lines = out.splitlines()[1:]  # preskoči header "List of devices attached"
    usb_devices = [line.split()[0] for line in lines if "\tdevice" in line and ":" not in line]

    if not usb_devices:
        print("❌ Nema pronađenih USB uređaja.")
        print("➡️  Provjeri da je mobitel spojen USB kabelom i da je uključeno USB debugging.")
        os.system("pause")   # ostavi prozor otvoren
        return

    serial = usb_devices[0]
    print(f"✅ Nađen USB uređaj: {serial}")

    print("▶️ Pokrećem scrcpy...")
    code, out, err = run_command(["scrcpy", "-s", serial])
    if code != 0:
        print("❌ Greška pri pokretanju scrcpy:", err or out)
    else:
        print("✅ scrcpy završen.")

    os.system("pause")   # drži prozor otvoren na kraju

if __name__ == "__main__":
    main()
