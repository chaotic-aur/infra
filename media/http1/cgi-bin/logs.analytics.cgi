#!/usr/bin/env bash
echo -e "Content-Type: application/json\nContent-Encoding: gzip\n"

# Settings
readonly IPv4_CENSOR='s/([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+)/\1.\2.???.\4/g'
readonly IPv6_CENSOR='s/(([[:xdigit:]]{,4}:)*)[[:xdigit:]]{,4}:[[:xdigit:]]{,4}$/\1??:??/g'
readonly LOCALHOST_FILTER='!/^(::1|localhost|127\.0\.0\.1)/v'
export LOGS_DIRECTORY='/var/log/httpd'
#[ ! -d "$LOGS_DIRECTORY" ] && export LOGS_DIRECTORY=''
TODAY="$(date --date='-1 month' +'%d\/%b')"

# Code
function read_logs() {
	## Enter
	pushd "$LOGS_DIRECTORY" > /dev/null

	## Metadata
	echo -n '{"metadata": { "first": "'
	### First entry time
	find . -type f -name "access*" -printf "%TY%Tm%Td%TH%TM%TS %p\n" |\
		sort | head -n 1 | awk '{print $2}' |\
		xargs head -n 1 | grep -Po '(?<=\[)([^\]])*' | head -c -1 
	### Last entry time
	echo -n '", "last": "'
	tail -n 1 access_log | grep -Po '(?<=\[)([^\]])*' | head -c -1
	### end metadata
	echo -n '"}'
	
	## Clean duplicates
	UNIQ_ACCESS=$(
		awk "$LOCALHOST_FILTER" ./access_log* |\
			awk '{print $1" "$7}' |\
			grep -Po '^([^ ]+ \/+chaotic-aur\/x86_64\/.*)(?=(?:-(?:[^-]*)){3}\.pkg\.tar\.(?:xz|zst)$)' |\
			sort -u
	)

	## Packages
	echo ',"downloads": ['
	echo "$UNIQ_ACCESS" |\
		awk '{print $2}' |\
		sort | uniq -c | sort -nr |\
		sed -r 's/^ *([^ ]+) \/+chaotic-aur\/x86_64\/(.+)$/{"count":"\1","name":"\2"},/g' |\
		grep -P '^{.*$' |\
		head -c -2
	echo -n ']'

	## 100 Users
	echo ',"users_top100": ['
	echo "$UNIQ_ACCESS" |\
		awk '!/::1/{print $1}' |\
		sort | uniq -c | sort -nr |\
		head -n 100 |\
		sed -r "$IPv4_CENSOR;$IPv6_CENSOR;s/^ *([^ ]+) (.+)$/{\"count\":\"\\1\",\"addr\":\"\\2\"},/g" |\
		head -c -2
	echo -n ']}'

	## Leave
	popd > /dev/null
}

read_logs | gzip -fc -
