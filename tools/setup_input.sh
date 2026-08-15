#!/usr/bin/env bash
# setup_input.sh — install ydotool for mouse control (the only capability the
# root-free hyprctl path cannot provide).
#
# You only need this if the automation must click: focusing a different in-game
# code window, pressing the ▶ button, or navigating menus. Keyboard-driven runs
# (write file -> F5 -> capture) work without it.
#
# Run interactively — it needs sudo. Do NOT leave this for the unattended loop.
set -euo pipefail

echo "==> installing ydotool"
sudo pacman -S --needed ydotool

echo "==> udev rule so your user can open /dev/uinput without root"
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-uinput.rules >/dev/null
sudo usermod -aG input "$USER"
sudo udevadm control --reload-rules && sudo udevadm trigger

echo "==> ydotoold user service"
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/ydotoold.service <<'EOF'
[Unit]
Description=ydotool daemon

[Service]
ExecStart=/usr/bin/ydotoold
Restart=always

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now ydotoold.service

cat <<'EOF'

==> done. Log out and back in for the 'input' group to take effect, then verify:

    systemctl --user status ydotoold
    ydotool mousemove -a -x 100 -y 100

Clicking the game then looks like:

    hyprctl dispatch focuswindow class:steam_app_2060160
    ydotool mousemove -a -x <X> -y <Y>
    ydotool click 0xC0        # left press+release

Coordinates are *logical* compositor pixels (the window reports 2048x1152),
while screenshots come back in native pixels (2560x1440). Divide screenshot
coordinates by 1.25 before feeding them to ydotool.
EOF
