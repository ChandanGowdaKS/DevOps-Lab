#!/bin/bash
set -e

echo "=========================================================="
echo "          Jenkins CI/CD Automation Pipeline               "
echo "=========================================================="
echo " Project Name  : DevOps Lab - Hello World Automation Job "
echo " Author        : Chandan Gowda K S                        "
echo " Host Machine  : $(hostname)                             "
echo " Current User  : $(whoami)                               "
echo " Executed Time : $(date '+%Y-%m-%d %H:%M:%S %Z')         "
echo " Status        : Build Stage Succeeded                    "
echo "=========================================================="
echo "Hello, World! Jenkins Job executed successfully from Git!"
