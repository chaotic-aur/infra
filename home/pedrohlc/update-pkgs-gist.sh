#!/usr/bin/env sh

cd /srv/http/chaotic-aur
cat pkgs.txt | gist -u fa294b4c490a363579cafa4a80b5b490 -f 'chaotic-pkgs.txt'
