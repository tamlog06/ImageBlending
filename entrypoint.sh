#!/bin/bash

export USER=builder
export HOME=/home/$USER

# find the uid and gid of the current directory
uid=$(stat -c "%u" .)
gid=$(stat -c "%g" .)

if [ "$uid" -ne 0 ]; then
    if [ "$(id -g $USER)" -ne $gid ]; then
        # if the gid of the builder user and current directory are different
        # then change the builder user's gid to the current directory's gid
        # and change the gid of the home directory
        getent group $gid >/dev/null 2>&1 || groupmod -g $gid $USER
        chgrp -R $gid $HOME
    fi
    if [ "$(id -u $USER)" -ne $uid ]; then
        # if the uid of the builder user and current directory are different
        # then change the builder user's uid to the current directory's uid
        usermod -u $uid $USER
    fi
fi

# this script is run as root, so we need to exec as the builder user
exec setpriv --reuid=$USER --regid=$USER --init-groups "$@"
