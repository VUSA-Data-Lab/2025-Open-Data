#!/bin/bash
# echo
# apt-get update -y

echo "Activating Python environment..."
apt-get install -y python3 python3-pip
pip install pandas matplotlib requests jupyterlab yfinance
echo "✅ Python ready!"
echo

echo "Activating PHP environment..."
sudo apt-get install -y php-cli composer
echo "✅ PHP ready!"
echo
