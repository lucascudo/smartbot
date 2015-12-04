#!/bin/bash

if [[ ! -d ENV ]]; then
	virtualenv ENV
fi

. ENV/bin/activate
pip install -r requirements.txt

echo
echo Now you can type:
printf "\e[0;32msource ENV/bin/activate\e[0m\n"
echo
