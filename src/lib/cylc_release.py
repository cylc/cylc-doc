#!/usr/bin/env python

from cylc.flow import __version__

from pkg_resources import parse_version


def pinned_version(version):
    """Return a short version suitible for pinning Cylc Flow in recipes.

    For most uses pinning to the minor version is likely the safest option::

       conda install cylc-flow=8.1

    For major pre-releases (e.g. 8.0b1) we keep the pre release tag.

    See https://github.com/cylc/cylc-admin/issues/130

    Examples:
        >>> pinned_version('8.0.1')
        '8.0'
        >>> pinned_version('8.0.1b1')
        '8.0'
        >>> pinned_version('8.0.1.dev')
        '8.0'
        >>> pinned_version('8.0b1')
        '8.0b1'
        >>> pinned_version('8.0b1.dev')
        '8.0b1'
        >>> pinned_version('8.0rc1')
        '8.0rc1'

    """
    ver = parse_version(version)
    if ver.pre and ver.minor == 0 and ver.micro == 0:
        # special handling of major version pre-releases
        ret = (ver.major, str(ver.minor) + ''.join(map(str, ver.pre)))
    else:
        ret = (ver.major, ver.minor)
    return '.'.join(map(str, ret))


CYLC_RELEASE = pinned_version(__version__)


if __name__ == '__main__':
    print(CYLC_RELEASE)
