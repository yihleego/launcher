# Launcher

## Introduction

Support WeChat, WeCom, DingTalk and custom applications.

## Usage

### Syntax

```shell
python launcher.py -a <app> -n <num> -p <path>
```

### Examples

1. Launch one WeChat client.

       python launcher.py -a wechat

2. Launch two WeChat clients.

       python launcher.py -a wechat -n 2

3. Launch one WeChat client with an alias. (More alias see: [config](/src/config.json))

       python launcher.py -a wx

4. Launch one WeChat client with a specified path.

       python launcher.py -a wechat -p C:\WeChat.exe

