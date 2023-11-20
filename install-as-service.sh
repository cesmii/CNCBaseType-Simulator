#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SVCNAME=cnc-sim
SVCSCRIPT=start-sim.sh
SVCARG="-o"

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

if [ $# -eq 0 ]; then
    SVCARG="$SVCARG 1"
    echo "Creating service with default name"
else
    SVCNAME=$SVCNAME$1
    SVCARG="$SVCARG $1"
    echo "Creating service with custom name: $SVCNAME.service"
fi
echo "  ExecStart will use: $SCRIPT_DIR/$SVCSCRIPT"
echo "  $SVCARG will be passed to the ExecStart script"
echo
read -p "Abort with CTRL+C, or press enter to continue..."

SVCNAME=$SVCNAME.service
if [ $(which systemctl) ]; then
    echo "Creating entry in /etc/systemd/system"
    SVCPATH=/etc/systemd/system/$SVCNAME
    echo "[Unit]" > $SVCPATH
    echo "Description=CNCBaseType Simulator" >> $SVCPATH
    echo "" >> $SVCPATH
    echo "[Service]" >> $SVCPATH
    echo "Type=simple" >> $SVCPATH
    echo "ExecStart=/bin/bash $SCRIPT_DIR/$SVCSCRIPT $SVCARG" >> $SVCPATH
    echo "" >> $SVCPATH
    echo "[Install]" >> $SVCPATH
    echo "WantedBy=multi-user.target" >> $SVCPATH

    echo "Reloading systemd"
    systemctl daemon-reload

    echo "Starting Service"
    systemctl enable $SVCNAME
    systemctl start $SVCNAME
else
    echo "systemd not found, service could not be installed"
fi
