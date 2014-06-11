#!/bin/bash

usage() {
    cat <<- EOF
    Usage: $0 [options]
           $0 --compile

    Options:
      -h, --help            show this help message and exit
      -p PORT, --port PORT  Port to start the server on.
      -i IP, --ip IP        IP address to listen on.
EOF
}

if [[ ! -d /usr/share/qwebirc ]]; then
    echo "ERROR: /usr/share/qwebirc does not exist!" >&2
    echo "It looks like your installation is incomplete." >&2
    exit 1
fi

if [[ ! -r /etc/qwebirc/config.py ]]; then
    echo "ERROR: /etc/qwebirc/config.py does not exist or is not readable!" >&2
    exit 1
fi

cd /usr/share/qwebirc

if [[ "$1" == '--compile' ]]; then
    echo "You can ignore warnings about mercurial."
    echo
    python2 compile.py
    exit $?
fi

options=('--logfile=/var/log/qwebirc/twisted.log'
         '--clf=/var/log/qwebirc/combined.log'
         '--pidfile=/run/qwebirc/qwebirc.pid')

if [[ -r /etc/qwebirc/ssl.key && -r /etc/qwebirc/ssl.cert ]]; then
    options+=('--certificate=/etc/qwebirc/ssl.cert'
              '--key=/etc/qwebirc/ssl.key')
fi

shift # $0
while :; do
    case "$1" in
        --help|-h|-\?)
            usage
            exit 0
            ;;
        -p|--port)
            options+=("-p" "$2")
            shift 1
            ;;
        -i|--ip)
            options+=("-i" "$2")
            shift 1
            ;;
        -*)
            echo "Unknown option $1!"
            usage
            exit 1
            ;;
        *) # no more options
            break
            ;;
    esac
done

python2 run.py "${options[@]}"
