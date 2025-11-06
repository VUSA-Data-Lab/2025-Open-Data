#!/bin/bash
echo
echo "Activating Python environment..."
pip install pandas matplotlib requests jupyterlab yfinance
echo "✅ Python ready!"
echo
echo "Activating PHP environment..."
sudo apt-get update -y
sudo apt-get install -y php-cli composer
echo "✅ PHP ready!"
echo
