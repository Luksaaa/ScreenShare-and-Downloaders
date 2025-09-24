import subprocess
import os

# 🔧 Postavi IP adresu i port tvog uređaja
DEVICE_IP = "192.168.1.202"
DEVICE_PORT = "45285"
DEVICE_ADDR = f"{DEVICE_IP}:{DEVICE_PORT}"

def run_command(cmd):
    """Pokreni komandu i vrati (kod, izlaz, error)."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def main():
    print("🔌 Diskonektiram sve veze...")
    run_command(["adb", "disconnect"])

    print(f"🌐 Pokušavam spojiti uređaj na {DEVICE_ADDR} ...")
    code, out, err = run_command(["adb", "connect", DEVICE_ADDR])
    if code != 0 or "connected" not in out.lower():
        print("❌ Greška kod spajanja:", err or out)
        os.system("pause")
        return

    print(f"✅ Spojen uređaj: {DEVICE_ADDR}")

    print("▶️ Pokrećem scrcpy...")
    code, out, err = run_command(["scrcpy", "-s", DEVICE_ADDR])
    if code != 0:
        print("❌ Greška pri pokretanju scrcpy:", err or out)
    else:
        print("✅ scrcpy završen.")

    os.system("pause")   # ostavi CMD otvoren na kraju

if __name__ == "__main__":
    main()
