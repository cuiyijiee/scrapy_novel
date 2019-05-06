#!/bin/bash

cd /home/scrapy_novel/zhuishubang
nohup python main.py>log.txt &
cd /home/scrapy_novel/biqugecc
nohup python main.py>log.txt &
