#!/usr/bin/env python

import plistlib
import subprocess

ppc_apps = []

command = ["system_profiler", "-xml", "SPApplicationsDataType"]
task = subprocess.Popen(command, stdout=subprocess.PIPE)
(stdout, unused_stderr) = task.communicate()

apps = plistlib.readPlistFromString(stdout)[0]["_items"]

for app in apps:
  if "runtime_environment" in app:
    if app["runtime_environment"] == "arch_ppc":
      ppc_apps.append(app["path"])

print "\n".join(ppc_apps)