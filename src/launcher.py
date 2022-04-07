# -*- coding: utf-8 -*-
import getopt
import os
import sys
import winreg

import psutil
import win32process
import yaml

import pywinhandle


def main(argv, configs: dict):
    app = None
    num = 1
    path = None
    try:
        opts, args = getopt.getopt(argv, "ha:n:p:", ["app=", "num=", "path="])
    except getopt.GetoptError:
        print('launcher -a <app> -n <number> -p <path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('launcher -a <app> -n <number> -p <path>')
            sys.exit()
        elif opt in ("-a", "--app"):
            app = arg
        elif opt in ("-n", "--num"):
            num = int(arg)
        elif opt in ("-p", "--path"):
            path = arg
    if not app:
        print(f"Invalid app")
        sys.exit(2)
    lower_name = app.lower()
    for name, config in configs.items():
        alias = config.get('alias', {})
        if lower_name == name or lower_name in alias:
            launch(num, path, config)
            sys.exit(0)
    print(f"Unsupported app '{app}'")
    sys.exit(2)


def launch(num, path, config):
    app_name = config.get('app_name')
    process_name = config.get('process_name')
    mutex_names = config.get('mutex_names')
    if not path or not os.path.exists(path):
        path = get_path(config.get('registry_key_name'), config.get('registry_value_name'))
    if not path:
        print(f"Cannot find path for '{app_name}'")
        return
    for i in range(num):
        if process_name and mutex_names:
            process_ids = []
            for proc in psutil.process_iter(attrs=['name']):
                if proc.info['name'] == process_name:
                    process_ids.append(proc.pid)
            if process_ids:
                handles = pywinhandle.find_handles(process_ids=process_ids, handle_names=mutex_names)
                pywinhandle.close_handles(handles)
        p = win32process.CreateProcess(path, '', None, None, 0, 0, None, None, win32process.STARTUPINFO())
        if p and len(p) > 1:
            print(f"[+] {app_name} ({p[2]}) OK!")


def get_path(key_name, value_name):
    if not key_name or not value_name:
        return None
    key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, key_name)
    values = winreg.QueryValueEx(key, value_name)
    if len(values) <= 0:
        return None
    path = values[0].strip()
    if path.startswith('\"') or path.startswith('\''):
        path = path[1:]
    if path.endswith('\"') or path.endswith('\''):
        path = path[:-1]
    return path


if __name__ == "__main__":
    configs = yaml.load(open(os.path.abspath('./config.yml'), 'r', encoding='utf-8'), Loader=yaml.SafeLoader)
    main(sys.argv[1:], configs.get('apps', {}))
