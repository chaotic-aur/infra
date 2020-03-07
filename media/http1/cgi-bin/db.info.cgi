#!/usr/bin/env bash
echo -e "Content-Type: application/json\nContent-Encoding: gzip\n"

# Settings
readonly REPO_DIRECTORY='/srv/http/chaotic-aur/x86_64'

# Code
function read_db() {
	## Enter
	pushd "$REPO_DIRECTORY" > /dev/null

	## Packages
	echo '{"packages": ['
	tar -tvzf chaotic-aur.db.tar.gz |\
		awk '/^d/{print $6}' |\
		sed -r 's/^(.+)-([^-]+)-([^-]+)\//{"name":"\1","ver":"\2","rel":"\3"},/g' |\
		head -c -2
	echo -n ']}'

	## Leave
	popd > /dev/null
}

read_db | gzip -fc -
