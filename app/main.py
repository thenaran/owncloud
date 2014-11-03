# -*- coding: utf-8 -*-
# Copyright 2012-2014 Narantech Inc.
#
# This program is a property of Narantech Inc. Any form of infringement is
# strictly prohibited. You may not, but not limited to, copy, steal, modify
# and/or redistribute without appropriate permissions under any circumstance.
#
#  __    _ _______ ______   _______ __    _ _______ _______ _______ __   __
# |  |  | |   _   |    _ | |   _   |  |  | |       |       |       |  | |  |
# |   |_| |  |_|  |   | || |  |_|  |   |_| |_     _|    ___|       |  |_|  |
# |       |       |   |_||_|       |       | |   | |   |___|       |       |
# |  _    |       |    __  |       |  _    | |   | |    ___|      _|       |
# | | |   |   _   |   |  | |   _   | | |   | |   | |   |___|     |_|   _   |
# |_|  |__|__| |__|___|  |_|__| |__|_|  |__| |___| |_______|_______|__| |__|

# default
import os
import os.path
import atexit
import subprocess
import logging

# clique
import clique.web
import clique.runtime

__FLAG__ = os.path.join(clique.runtime.home_dir(), "_check")


def start():
  if not os.path.exists(__FLAG__):
    cmd = "sh {script}; touch {flag}".format(script=os.path.join(clique.runtime.res_dir(),
                                                                 "prepare.sh"),
                                             flag=__FLAG__)
    try:
      subprocess.check_call(cmd, shell=True)
      logging.info("Success execute prepare script.")
    except:
      logging.warn("Failed to execute prepare script.", exc_info=True)
      if os.path.exists(__FLAG__):
        subprocess.check_call("rm {flag}".format(flag=__FLAG__), shell=True)

  clique.web.set_static_path(os.path.join(clique.runtime.res_dir(), "web"))
  subprocess.check_call('sudo /etc/init.d/php5-fpm start', shell=True)
  subprocess.check_call('/etc/init.d/nginx start', shell=True)
  logging.info("The daemon services (nginx, php5) started.")


@atexit.register
def stop():
  logging.info("stopping the daemon services (nginx, php5)...")
  subprocess.check_call('sudo /etc/init.d/php5-fpm stop', shell=True)
  subprocess.check_call('/etc/init.d/nginx stop', shell=True)


if __name__ == "__main__":
  start()
