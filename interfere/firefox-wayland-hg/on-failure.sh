#!/usr/bin/env sh
[ -f ../firefox-wayland-hg.log ] && \
telegram-send \
	--config ~/.config/telegram-send-group.conf \
	--sile "[BOT ALERT] @thotypous your package \"firefox-wayland-hg\" build failed, here's the log: " \
	-f ../firefox-wayland-hg.log
