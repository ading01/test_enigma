#!/bin/bash
coverage run --branch --source . -m pytest && coverage report