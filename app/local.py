#
# Copyright 2014 Narantech Inc.

# This program is a property of Narantech Inc. Any form of infringement is
# strictly prohibited. You may not, but not limited to, copy, steal, modify # and/or redistribute without appropriate permissions under any circumstance.
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
import logging
import subprocess

# clique
from clique import Lazy

# owncloud
import util


__DATA__ = Lazy()
__DATA__.add_initializer("config", lambda: _config())

#__CLASS_KEY__ = '''user.all.\/$user\/files\/{folder_name}.class'''
__CLASS_KEY__ = '''user.all./$user/files/{folder_name}.class'''
__CLASS_VALUE__ = '''\\OC\\FileS\\Storage\\Local'''
#__OPTION_KEY__ = '''user.all.\/$user\/files\/{folder_name}.options.datadir'''
__OPTION_KEY__ = '''user.all./$user/files/{folder_name}.options.datadir'''
__OPTION_VALUE__ = '''{path}'''

__SETTINGS_PATH__ = '''/var/www/owncloud/data/mount.json'''
__USER__ = '''www-data'''
__GROUP__ = '''owncloud'''


def _config():
  if not os.path.exists(__SETTINGS_PATH__):
    cmd = "sudo touch {path};sudo chmod 777 {path}; sudo chown {user}:{group} {path}".format(path=__SETTINGS_PATH__,
                                                                                             user=__USER__,
                                                                                             group=__GROUP__)
    try:
      subprocess.check_call(cmd, shell=True)
    except:
      logging.warn("Failed to execute cmd. Cmd : %s", cmd, exc_info=True)

  return util.Settings([__SETTINGS_PATH__])


def add_local_storage(path):
  if os.path.exists(os.path.dirname(__SETTINGS_PATH__)):
    subprocess.check_call("sudo chmod 777 {path}".format(path=os.path.dirname(__SETTINGS_PATH__)),
                          shell=True)
  folder_name = os.path.basename(path)
  class_key = __CLASS_KEY__.format(folder_name=folder_name)
  class_value = __CLASS_VALUE__
  option_key = __OPTION_KEY__.format(folder_name=folder_name)
  #option_value = __OPTION_VALUE__.format(path=path.replace("/", "\/"))
  option_value = __OPTION_VALUE__.format(path=path)
  __DATA__.config.set(class_key, class_value)
  __DATA__.config.set(option_key, option_value)
  __DATA__.config.flush()
  logging.info("Add local storage. path : %s", path)
  

def remove_local_storage(path):
  if os.path.exists(os.path.dirname(__SETTINGS_PATH__)):
    subprocess.check_call("sudo chmod 777 {path}".format(path=os.path.dirname(__SETTINGS_PATH__)),
                          shell=True)
  folder_name = os.path.basename(path)
  tmp_dict = __DATA__.config.get_symbol()
  collect_key = []
  for key in tmp_dict.keys():
    if folder_name in key:
      collect_key.append(key)

  for key in collect_key:
    if key in tmp_dict:
      del tmp_dict[key]

  __DATA__.config.reset()

  for key, value in tmp_dict.items():
    __DATA__.config.set(key, value) 

  __DATA__.config.flush()
  logging.info("Remove local storage. path : %s", path)
