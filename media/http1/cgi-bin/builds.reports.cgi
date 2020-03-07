#!/usr/bin/env bash
if [ ! -d "/home/main-builder" ]; then
	echo -n "Status: 404 Not Found\n" \
		"Content-Type: text/html\n\n" \
		'<h1>404 File not found!</h1>'
	exit
fi

echo -e "Content-Type: application/json\nContent-Encoding: gzip\n"

# Settings
export LOGS_DIRECTORY='/srv/http/chaotic-aur/makepkglogs'
#[ ! -d "$LOGS_DIRECTORY" ] && export LOGS_DIRECTORY=''

# Code
function build_report() {
	## Enter
	pushd "$LOGS_DIRECTORY" > /dev/null

	## Failing
	### Hourly
	echo -n '{"failing": {"hourly": "'
	echo -n $(expr $(ls -1 *.log | wc -l) - 2)
	### Daily
	echo -n '", "daily": "'
	echo -n $(expr $(ls -1 _daily/*.log | wc -l) - 2)
	### TKG
	echo -n '", "tkg": "'
	echo -n $(ls -1 _daily/tkg/*.log | wc -l)
	### TKG (Kernels)
	echo -n '", "tkg.kernels": "'
	echo -n $(ls -1 _daily/tkg/kernels/*.log | wc -l)
	### Cubocore
	echo -n '", "cubocore": "'
	echo -n $(expr $(ls -1 _daily/cubocore_/*.log | wc -l) - 1)
	### Librewish
	echo -n '", "librewish": "'
	echo -n $(expr $(ls -1 _daily/librewish/*.log | wc -l) - 1)
	### Flighlessmango
	echo -n '", "mango": "'
	echo -n $(expr $(ls -1 _daily/flightlessmango/*.log | wc -l) - 1)
	### end failing
	echo -n '"}'

	## Services
	echo -n ', "services": {'
	### Hourly
	echo -n '"hourly": {'
	get_service 'build-hourly'
	### Morning
	echo -n '}, "morning": {'
	get_service 'build-morning'
	### Sunset
	echo -n '}, "sunset": {'
	get_service 'build-sunset'
	### Nightly
	echo -n '}, "nightly": {'
	get_service 'build-night'
	### TkG-Kernels
	echo -n '}, "tkg.kernels": {'
	get_service 'build-tkg-kernels'
	echo -n '}}}'
	
	## Leave
	popd > /dev/null
}

function get_service() {
	echo -n '"status": "'
	systemctl is-active "$1.service" | head -c -1
	echo -n '", "scheduled": "'
	systemctl is-active "$1.timer" | head -c -1
	echo -n '"'
}

build_report | gzip -fc -
