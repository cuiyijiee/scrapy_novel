#!/usr/bin/env bash
cd /home/scrapy_novel

nohup python3.7 biqugecc.py>log/biqugecc.txt 2>&1 &
nohup python3.7 zhuishubang.py>log/zhuishubang.txt 2>&1 &
nohup python3.7 i7wx.py>log/i7wx.txt 2>&1 &
nohup python3.7 luoqiu_pc.py>log/luoqiu.txt 2>&1 &
nohup python3.7 du00.py>log/du00.txt 2>&1 &
nohup python3.7 jinjiang.py>log/jinjiang.txt 2>&1 &
nohup python3.7 xbiquge6.py>log/xbiquge6.txt 2>&1 &
nohup python3.7 bbiquge.py>log/bbiquge.txt 2>&1 &