#!/usr/bin/env python3

import json
import re

import requests

# Grab the latest project versions that have been published to copr, and
# write them to a local file suitable for importing and passing to
# kubevirt/libvirt container build

URL = "https://copr.fedorainfracloud.org/api_2/projects?group=kubevirt"
RAWDATA = json.loads(requests.get(URL).content)
ALL_PROJECT_NAMES = [p["project"]["name"] for p in RAWDATA["projects"]]


def natural_sort(lst):
    # https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(lst, key=alphanum_key)


def find_latest(projname):
    names = [n for n in ALL_PROJECT_NAMES if n.startswith(projname)]
    for verrel in reversed(natural_sort(names)):
        if ".el" in verrel:
            # Ignore any RHEL rebuilds. We always want to use Fedora builds
            # for this container
            continue
        return verrel.split("-", 1)[1]


out = ""
out += """export LIBVIRT_VERSION="%s"\n""" % find_latest("libvirt")
out += """export QEMU_VERSION="%s"\n""" % find_latest("qemu")
out += """export SEABIOS_VERSION="%s"\n""" % find_latest("seabios")
print("Generated: \n%s" % out)
filename = "container_versions"
open(filename, "w").write(out)
print("Wrote to '%s'" % filename)
