# /bin/bash
set -e

if ((EUID == 0)); then
  echo >&2 "Error: script should not running as root or with sudo! Exiting..."
  exit 1
fi

git pull
python3 tests.py
echo 'about to kill old process'
pgrep -af 'python.*\s+web.py' || echo "old process not found"
pkill -f 'python.*\s+web.py' || echo "old process not found"
echo 'starting server'
python3 web.py 2>/dev/null &
