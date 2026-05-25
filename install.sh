echo "Installing tamo-cli"

sudo cp src/tamo.py /usr/local/bin/tamo
echo "Copied tamo.py"

sudo mkdir -p /etc/tamo-cli
sudo cp tamo-cli-conf-example.json /etc/tamo-cli/tamo-cli-conf.json
echo "Created config file"

sudo cp -r src/TamoAPI /usr/local/lib/tamo-cli
echo "Copied TamoAPI (huge thanks to justinas2314 on GitHub)"

sudo chmod +x /usr/local/bin/tamo # make it executable

echo "Installed tamo-cli."
echo "Go configure it in /etc/tamo-cli/tamo-cli-conf.json"