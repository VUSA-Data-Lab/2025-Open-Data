#!/bin/bash
echo "----------------------------------------"
echo "Welcome to VUŠA Open Data Lab!"
echo "Please choose your environment:"
echo "1) Python"
echo "2) PHP"
echo "----------------------------------------"
read -p "Enter number (1 or 2): " choice

if [ "$choice" = "1" ]; then
  echo "Activating Python environment..."
  pip install pandas matplotlib requests jupyterlab
  echo "✅ Python ready!"
elif [ "$choice" = "2" ]; then
  echo "Activating PHP environment..."
  sudo apt-get update -y
  sudo apt-get install -y php-cli composer
  echo "✅ PHP ready!"
else
  echo "❌ Invalid choice. Please restart Codespace."
fi
