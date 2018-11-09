#
# ~/.bashrc
#

# If not running interactively, don't do anything
unset HISTFILE
alias rm='/usr/local/bin/rm.safe'

[[ $- != *i* ]] && return

alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '
