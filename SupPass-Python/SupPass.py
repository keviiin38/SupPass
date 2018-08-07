#
#    SupPass -- No Credentials Storage. No Problem.
#
#    Copyright (C) 2018 Kevin Delbegue, 2O4, Yann Loukili, Mathieu Calemard Du Gardin
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

#!/usr/bin/python3

import sys
import argparse
import base64
import hashlib
import platform, os  # for the clipboard function
import time


def build_password(input_data):
    password = ''
    input_data_hashed = hashlib.sha256(input_data.encode()).hexdigest()  # Hash the input_data with SHA-256

    for i in range(0, 64, 4):
        password += input_data_hashed[i]  # Select 1 char every 4 chars on a 64 chars string (total of 16 chars)

    password = base64.b64encode(password.encode()).decode()  # Convert to Base64, add Upper and Lower case

    return password[:16]  # Return only the 16 first characters of the Base64 result


def copy_clipboard(text):
    text = str(text)

    def winClip(text):
        command = 'echo | set /p nul=' + text.strip() + '| clip'
        os.system(command)


    def macClip(text):
        outf = os.popen('pbcopy', 'w')
        outf.write(text)
        outf.close()


    def gtkClip(text):
        global cb
        cb = gtk.Clipboard()
        cb.set_text(text)
        cb.store()


    def qtClip(text):
        cb.setText(text)


    def xclipClip(text):
        outf = os.popen('xclip -selection c', 'w')
        outf.write(text)
        outf.close()


    def xselClip(text):
        outf = os.popen('xsel -i', 'w')
        outf.write(text)
        outf.close()


    if os.name == "nt" or platform.system() == "Windows":
        import ctypes
        winClip(text)
    elif os.name == "mac" or platform.system() == "Darwin":
        macClip(text)
    elif os.name == "posix" or platform.system() == "Linux":
        xclipExists = os.system("which xclip") == 0
        if xclipExists:
            xclipClip(text)
        else:
            xselExists = os.system("which xsel") == 0
            if xselExists:
                xselClip(text)
            try:
                import gtk
                gtkClip(text)
            except Exception:
                try:
                    import PyQt4.QtCore
                    import PyQt4.QtGui
                    app = PyQt4.QApplication([])
                    cb = PyQt4.QtGui.QApplication.clipboard()
                    qtClip(text)
                except:
                    raise Exception("SupPass python requires the gtk or PyQt4 module installed,\n"
                                    "or the xclip command to copy to clipboard")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--username', help="Input username for the site", action="store", type=str, nargs="?")
    parser.add_argument('-d', '--domain',   help="Domain name", action="store", type=str, nargs="?")
    parser.add_argument('-p', '--password', help="Master password", action="store", type=str, nargs="?")
    parser.add_argument('-s', '--see',      help="Enable the print of the password", action="store_true")
    parser.add_argument('-c', '--clipoff',  help="Disable the copy in clipboard", action="store_true")
    parser.add_argument('-t', '--timer',    help="Timer before flushing the clipboard", action="store", type=int, nargs="?", default=60)

    args = parser.parse_args()
    username = args.username
    domain = args.domain
    password = args.password
    SEE = args.see
    CLIPOFF = args.clipoff
    timer = args.timer

    if username==None or password==None or domain==None:
        print("./SupPass.py -u <username> -d <domain_name> -p <master_password>")

    final_password = build_password(username + domain + password)

    if SEE:
        print("\nYour password:", final_password, "\n")

    if not(CLIPOFF):
        copy_clipboard(final_password)
        if timer>0:
            time.sleep(timer)
            copy_clipboard('')
