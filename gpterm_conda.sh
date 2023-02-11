#!/bin/bash

if [[ $CONDA_DEFAULT_ENV != "gpterm" ]]; then
	conda activate gpterm
fi
gpterm
