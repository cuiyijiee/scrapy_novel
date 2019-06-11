#!/usr/bin/env bash
cd /home/scrapy_novel

nohup python3.7 biqugecc.py>log.txt 2>&1 &
nohup python3.7 zhuishubang.py>log.txt 2>&1 &
nohup python3.7 i7wx.py>log.txt 2>&1 &
nohup python3.7 luoqiu.py>log.txt 2>&1 &