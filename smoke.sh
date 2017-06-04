#!/bin/sh

set -eu

tarball="$1"
shift

yarn smoke.yarn --env ROOTFS_TARBALL="$tarball" "$@"
