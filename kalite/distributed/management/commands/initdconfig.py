"""
"""
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

script_template = """
#! /bin/sh

# Author: Jamie Alexandre, 2012
#
# /etc/init.d/kalite

### BEGIN INIT INFO
# Provides:          kalite
# Required-Start:    $local_fs $remote_fs $network $syslog $named
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: ka-lite daemon, a local Khan Academy content server
### END INIT INFO

case "$1" in
    start)
        echo "Starting ka-lite!"
        #run ka-lite as the owner of the project folder, and not as root
        su `stat --format="%%U" "%(repo_path)s"` -c "%(script_path)s/start.sh"
        ;;
    stop)
        echo "Shutting down ka-lite!"
        echo
        "%(script_path)s/stop.sh"
        ;;
esac

"""

if sys.platform == 'darwin':
    script_template = """
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>KA Lite Daemon</string>
        <key>Program</key>
        <string>%(script_path)s/start.sh</string>
        <key>RunAtLoad</key>
        <true/>
        <key>StandardOutPath</key>
        <string>/tmp/kalite.out</string>
        <key>StandardErrorPath</key>
        <string>/tmp/kalite.err</string>
        <key>WorkingDirectory</key>
        <string>%(repo_path)s</string>
    </dict>
</plist>
    """

    script_template = """
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>KA Lite Daemon</string>
        <key>Program</key>
        <string>su `stat -f "%%Su" "%(repo_path)s"` -c "%(script_path)s/start.sh"</string>
        <key>RunAtLoad</key>
        <true/>
        <key>StandardOutPath</key>
        <string>/tmp/kalite.out</string>
        <key>StandardErrorPath</key>
        <string>/tmp/kalite.err</string>
        <key>WorkingDirectory</key>
        <string>%(repo_path)s</string>
    </dict>
</plist>
    """


class Command(BaseCommand):
    help = "Print init.d startup script for the server daemon."

    def handle(self, *args, **options):
        # if [item for item in args if item.lower() == 'start']:
        #     print '==> args', args, ' ==> options', options
        repo_path = os.path.join(settings.PROJECT_PATH, "..")
        script_path = os.path.join(repo_path, "scripts")
        self.stdout.write(script_template % {"repo_path": repo_path, "script_path": script_path})
