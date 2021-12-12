#!/bin/zsh

[ -d "$HOME/.local/mnt/pi/home" ] || echo raspberry | sshfs pi@192.168.5.37:/ $HOME/.local/mnt/pi -o password_stdin
[ -d "$HOME/.local/mnt/pi2/home" ] || echo raspberry | sshfs pi@192.168.5.38:/ $HOME/.local/mnt/pi2 -o password_stdin

rm -r ~/.local/mnt/pi/home/pi/src
rm -r ~/.local/mnt/pi2/home/pi/src

cp -r ~/Projects/KayaExercizePiCode/ ~/.local/mnt/pi/home/pi/src
cp -r ~/Projects/KayaExercizePiCode/ ~/.local/mnt/pi2/home/pi/src
