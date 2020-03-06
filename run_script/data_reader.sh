#!/bin/bash
pytest -v
sleep 0.3
python data_reader/data_reader_main.py
