#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

APP_DIR="$HOME/.mimi"
BIN_DIR="$PREFIX/bin"
SOURCE_URL="${MIMI_SOURCE_URL:-https://raw.githubusercontent.com/Karlfiner-Robotiken/mimi/main/mimi.py}"

printf '\033[1;35m\nMIMI AI\n\033[0m'
printf '\033[1;36m[*] Preparing Termux dependencies...\033[0m\n'
pkg update -y
pkg install -y python python-pip nodejs curl figlet termux-api
pip install --upgrade rich pyfiglet
npm install -g tgpt

mkdir -p "$APP_DIR/memory" "$APP_DIR/logs" "$APP_DIR/plugins"

printf '\033[1;36m[*] Installing MIMI from %s...\033[0m\n' "$SOURCE_URL"
tmp_file="$(mktemp)"
trap 'rm -f "$tmp_file"' EXIT
curl --fail --location --silent --show-error "$SOURCE_URL" -o "$tmp_file"
python -m py_compile "$tmp_file"
install -m 0644 "$tmp_file" "$APP_DIR/mimi.py"

cat > "$BIN_DIR/mimi" <<'LAUNCHER'
#!/data/data/com.termux/files/usr/bin/bash
exec python "$HOME/.mimi/mimi.py" "$@"
LAUNCHER
chmod 0755 "$BIN_DIR/mimi"

if [ ! -f "$APP_DIR/settings.json" ]; then
  cat > "$APP_DIR/settings.json" <<'JSON'
{
    "theme": "neon",
    "voice": true,
    "memory": true,
    "animations": true,
    "auto_update": true
}
JSON
fi

printf '\033[1;32m[+] MIMI installed successfully.\033[0m\n'
printf 'Launch with: mimi\n'
if [ "${MIMI_NO_LAUNCH:-0}" != "1" ]; then
  exec "$BIN_DIR/mimi"
fi
