#!/bin/bash

if [[ -d ENV ]]; then
	virtualenv ENV
fi

source ENV/bin/activate
