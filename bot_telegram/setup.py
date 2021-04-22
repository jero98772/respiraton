#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
from setuptools import setup, find_packages
from tools.tools import writetxt
setup(
	name='Bot de Aire al parque',
	version='1.0.0',
	license='GPLv3',
	author_email='',
	author='Alianza piranga',
	description='',
	url='https://t.me/respirabot_bot',
	packages=find_packages(),
    install_requires=['python-telegram-bot'],
    include_package_data=True,
	)
print("recuerde añadir el token en bot_telegram/files/token.txt")
writetxt("bot_telegram/files/token.txt","telegram token aqui")