#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
from setuptools import setup, find_packages
from tools.tools import writetxt
setup(
	name='Consultor de Aire al parque',
	version='1.0.0',
	license='GPLv3',
	author_email='alianzapiranga@gmail.com',
	author='Alianza piranga',
	description='Consultor de predicciones de calidad de aire para sesnores Canairio y AQA',
	url='localhost:9600',
	packages=find_packages(),
    install_requires=['Flask', 'influxdb', 'matplotlib','statsmodels'],
    include_package_data=True,
	)
