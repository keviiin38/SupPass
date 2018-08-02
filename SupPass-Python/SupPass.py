#
#    SupPass -- No Credentials Storage. No Problem.
#
#    Copyright (C) 2018 Kevin Delbegue, Johnny201, Yann Loukili, Mathieu Calemard Du Gardin
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

import base64
import getopt
import hashlib
import sys
import platform, os  # for the clipboard function


def display_usage():
    print("SupPass -- The Safest Password Manager\n\n"
          "Usage : ./SupPass.py -u <username> -d <domain_name> -p <master_password>\n\n"
          "Options :\n"
          "     -h, --help      : show the help\n"
          "     -u, --username  : input username for the site (pseudo, mail, etc...)\n"
          "     -d, --domain    : domain name of the site\n"
          "     -p, --password  : master password of the user\n\n")
    sys.exit(1)


def get_options():
    try:
        options, arguments = getopt.getopt(sys.argv[1:], 'hu:d:p:', ['help', 'username=', 'domain=', 'password='])
        return options
    except getopt.GetoptError:
        return -1


def set_options(options):
    username, domain, password = "", "", ""

    for option, argument in options:
        if option in ('-h', '--help'):
            display_usage()
        elif option in ('-u', '--username'):
            username = argument
        elif option in ('-d', '--domain'):
            domain = argument
        elif option in ("-p", "--password"):
            password = argument

    if "" in (username, domain, password):
        display_usage()
    else:
        return username, domain, password


def build_password(input_data):
    password = ""
    input_data_hashed = hashlib.sha256(input_data.encode()).hexdigest()  # Hash the input_data with SHA-256

    for i in range(0, 60, 4):
        password += input_data_hashed[i]  # Select 1 char every 4 chars on a 60 chars string (total of 15 chars)

    password = base64.b64encode(password.encode()).decode()  # Convert to Base64, add Upper and Lower case

    return password[:15]  # Return only the 15 first characters of the Base64 result


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


def SupPass():
    options = get_options()

    if options == -1 or options == []:
        display_usage()

    username, domain, password = set_options(options)

    final_password = build_password(username + domain + password)

    print("\nYour password :", final_password, "\n"
          "do you want to copy it to your clipboard (y/n)")

    clip = str(input())

    if clip == "y" or "Y":  # this will copy the password to the clip board
        copy_clipboard(final_password)


SupPass()
