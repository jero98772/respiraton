#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
from setuptools import setup, find_packages
from tools.tools import writetxt
setup(
	name='',
	version='1.0.0',
	license='',
	author_email='',
	author='',
	description='',
	url='',
	packages=find_packages(),
    install_requires=['Flask', 'influxdb', 'matplotlib','statsmodels'],
    include_package_data=True,
	)
print("recuerde añadir el token en bot_telegram/files/token.txt")
writetxt("bot_telegram/files/token.txt","telegram token aqui")