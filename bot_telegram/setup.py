#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
from setuptools import setup, find_packages
from scripts.tools import writetxt
setup(
	name='',
	version='1.0.0',
	license='',
	author_email='',
	author='',
	description='',
	url='',
	packages=find_packages(),
    install_requires=['python-telegram-bot'],
    include_package_data=True,
	)
print("recuerde añadir el token en bot_telegram/files/token.txt")
writetxt("bot_telegram/files/token.txt","telegram token aqui")