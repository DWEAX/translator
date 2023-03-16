# Install or update needed software
apt-get update
apt-get install -yq git supervisor python python-pip python3-distutils
pip install --upgrade pip virtualenv

# Fetch source code
export HOME=/root
git clone https://github.com/GoogleCloudPlatform/getting-started-python.git /opt/app
git clone https://github.com/DWEAX/translator.git /opt/app/translator

# Install Cloud Ops Agent
sudo bash /opt/app/gce/add-google-cloud-ops-agent-repo.sh --also-install

# Account to own server process
useradd -m -d /home/pythonapp pythonapp

# Python environment setup
virtualenv -p python3 /opt/app/translator/env
/bin/bash -c "source /opt/app/translator/env/bin/activate"
/opt/app/translator/env/bin/pip install -r /opt/app/translator/requirements.txt

# Set ownership to newly created account
chown -R pythonapp:pythonapp /opt/app

# Put supervisor configuration in proper place
cp /opt/app/gce/python-app.conf /etc/supervisor/conf.d/python-app.conf

# Start service via supervisorctl
supervisorctl reread
supervisorctl update
