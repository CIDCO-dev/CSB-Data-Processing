#!/usr/bin/python3.5

# ----------------------------------------------------------------------------------------------------------------------
# NAME: csrs_ppp_cgi_browser.py
# FUNCTION: To replace the use of a browser for submission of RINEX files to CSRS-PPP
# MODIFICATION/CREATION
# DATE          WHO     DESCRIPTION
# 2017-07-25    JF      1.1
# Modified:
#   2017-11-02
#       Made working directory a command line argument
#       Added verification for command line arguments lang, ref, mode
#       Added epoch verification
#       Used new string formatting
#
# How run to this script by itself
# --------------------------------
# 0) Requirements:
#       Python v3.5.x or higher
#       Requests library, v2.18.1 or higher
#       Requests Toolbelt library, v0.8.0 or higher
# 1) On the command line:
#   => csrs_ppp_cgi_browser.py --user_name cgis0172 --lang en --ref ITRF --epoch CURR --mode Static --rnx rnxfile --path work_dir
#   where:
#       rnxfile looks like ALGO2390.15o, $P/ABCD/ALGO2390.15d.Z, or simply ALGO2390.15d.Z if rnxfile is in current path!
#           and
#       work_dir is the absolute path of the directory holding the RINEX observation file
# ----------------------------------------------------------------------------------------------------------------------
#ie. python csrs_ppp_cgi_browser --user_name k.a@unb.ca --lang en --ref NAD83 --epoch CURR --mode Kinematic --rnx C:/PPP/13_46_34-2017_09_22-gps.17o --path C:/PPP

# Imports
# -------
import os
import sys
from subprocess import Popen, PIPE
import time
import argparse
import shlex
import datetime

try:
    import requests
except ImportError:
    sys.exit('ERROR: Must install Requests library\n\t(see http://docs.python-requests.org/en/master/)')
try:
    from requests_toolbelt.multipart.encoder import MultipartEncoder
except ImportError:
    sys.exit('ERROR: Must install Requests Toolbelt library\n\t(see https://toolbelt.readthedocs.io/en/latest/)')

# Read/set options
# ----------------
# Instantiate the parser
parser = argparse.ArgumentParser(description='Using CSRS-PPP via script')
# Required positional arguments
parser.add_argument('--user_name', required=True, help='User name / Utilisateur', type=str)
parser.add_argument('--lang', required=True, help='Language / Langue', type=str, choices=['en', 'fr'])
parser.add_argument('--ref', required=True, help='Reference frame / Cadre de r\u00e9f\u00e9rence', type=str,
                    choices=['NAD83', 'ITRF'])
parser.add_argument('--epoch', required=True, help='NAD83 epoch / \u00e9poque', type=str)
parser.add_argument('--mode', required=True, help='Processing mode / Mode de traitement', type=str,
                    choices=['Static', 'Statique', 'Kinematic', 'Cinematic', 'Cin\u00e9matic'])
parser.add_argument('--rnx', required=True, help='RINEX observation file / Fichier d\'observation RINEX', type=str)
parser.add_argument('--path', required=True, help='Absolute path of directory holding RINEX file / '
                                                  'Chemin d\'acc\u00e8s du r\u00e9pertoire contenant le fichier RINEX',
                    type=str)
# Parse arguments
args = parser.parse_args()

# Verify date format
# ------------------
if 'CURR' not in args.epoch and 'COUR' not in args.epoch:
    min_date = datetime.datetime.strptime('1997-01-01', '%Y-%m-%d').date()
    max_date = datetime.date.today()
    try:
        input_date = datetime.datetime.strptime(args.epoch, '%Y-%m-%d').date()
    except ValueError as e:
        sys.exit('ERROR: Invalid epoch: {0:s}'.format(args.epoch))

    if input_date > max_date:
        sys.exit('ERROR: Epoch cannot be later than today\'s date:'
                 '\n\tepoch chosen: {0:s}\n\ttoday\'s date: {1}'.format(args.epoch, max_date))

# Working directory
# -----------------
try:
    os.chdir(args.path)
except FileNotFoundError:
    sys.exit('ERROR: Cannot access directory {0:s}'.format(args.path))

# Useful var
# ----------
procstat = None

# Local Vars
# ----------
error = 0
debug = 0
sleepsec = 10
wget_options = '-q --tries=2 --timestamping --timeout=5'

request_max = 5
wget_max = 35

keyid = None

# Specify the URL of the page to post to
# --------------------------------------
url_to_post_to = 'http://webapp.geod.nrcan.gc.ca/CSRS-PPP/service/submit'
browser_name = 'CSRS-PPP access via Python-CGI Browser Emulator'

# Define PPP access mode
# ----------------------
ppp_access = 'nobrowser_status'  # default starting 2013-Sep-30

# Define possible cmd line options
sysref = 'NAD83'
nad83_epoch = 'CURR'  # (other possible values are 19970101 and 20020101)
process_type = 'Static'
# user_name = '_not_defined_'

# Print Info
# ----------
rinex_file_abspath = os.path.abspath(args.rnx)

(rinex_path, rinex_file) = os.path.split(rinex_file_abspath)

# Ensure splitting up the absolute path produces a file name and not just a directory
if rinex_file is None:
    sys.exit('ERROR: No RINEX file')
(rinex_name, suffix) = os.path.splitext(rinex_file)

name = rinex_name  # for later use!
print('=> RNX: {0:s} [{1:s}]'.format(rinex_file, rinex_path))

# Some more initializations
# -------------------------
if args.epoch == 'CURR' or args.epoch == 'COUR':
    nad83_epoch = 'CURR'
else:
    nad83_epoch = args.epoch

if args.mode == 'Static' or args.mode == 'Statique':
    process_type = 'Static'
else:
    process_type = 'Kinematic'

# -------------------------------------------------
# Create the browser that will post the information
# -------------------------------------------------
# ITERATE up to request_max!

for request_num in range(request_max):
    print('=> Request_num[{0:d}]'.format(request_num))

    # The information to POST "to the CGI program"
    content = {
        'return_email': 'dummy_email',
        'cmd_process_type': 'std',
        'ppp_access': ppp_access,
        'sysref': args.ref,
        'nad83_epoch': nad83_epoch,
        'process_type': process_type,
        'language': args.lang,
        'user_name': args.user_name,
        'rfile_upload': (rinex_file, open(rinex_file, 'rb'), 'text/plain')
    }
    mtp_data = MultipartEncoder(fields=content)
    # Insert the browser name, if specified
    header = {'User-Agent': browser_name, 'Content-Type': mtp_data.content_type, 'Accept': 'text/plain'}

    req = requests.post(url_to_post_to, data=mtp_data, headers=header)
    keyid = str(req.text)  # The keyid required for the job

    my_req = requests.get(url_to_post_to)

    html_tag = None
    html_data = None
    count = 0
    tag_data = None

    # Print some values for debug!
    if debug:
        print('Key: {0:s}'.format(req.text))

    # 'key'
    if req.text:
        keyid = req.text

        # Problems while doing the 'request'
        # ----------------------------------
        # Re-Submit!
        if 'DOCTYPE' in keyid:
            print('=> Hash{{_content}} has a weird value! [{0:s}]'.format(rinex_name))
            if debug:
                print('{0:s}'.format(keyid))
            print('=> Re-Submit ...')
            continue
        # key OKAY!
        # ---------
        print('=> Keyid: {0:s}'.format(keyid))
        print('=> Now wait until "Status=done" ...')

        # All is OKAY... now wait!
        # ------------------------
        # Initialize ...
        command = 'wget {0:s} -O Status.txt "http://webapp.geod.nrcan.gc.ca/CSRS-PPP/service/results/status?id={1:s}"'.format(wget_options, keyid)
        if debug:
            print('# {0:s}'.format(command))

        # -----------------
        # Loop until "done"
        # -----------------
        wget_num = 0
        if os.path.isfile('Status.txt'):
            os.remove('Status.txt')

        while not (procstat == 'done' or error == 1):
            wget_num += 1

            # Check wget_max
            if wget_num > wget_max:
                print('=> Max number of wget [{0:d}] exceeded! Too long! [{1:s}]'.format(wget_max, rinex_name))
                print('=> Next file ...')
                error = 1
                sys.exit(error)

            # wget 'Status.txt'
            # get the text output of the command...

            #import pdb; pdb.set_trace()

            log = Popen(shlex.split(command), stdout=PIPE)
            # ...and store it in a variable to parse later
            output = log.communicate()
            output = output[0].decode('utf-8')
            if output and debug:
                print('log[{0:d}]: {1:s}'.format(wget_num, log))

            # Check 'Status.txt'
            if os.path.isfile('Status.txt'):
                with open('Status.txt') as f:
                    status = f.readlines()

                # Read 'Status.txt'
                if 'processing' in str(status).lower():
                    procstat = 'processing'
                    sleepmore = 1
                elif 'done' in str(status).lower():
                    procstat = 'done'
                    sleepmore = 0
                elif 'error' in str(status).lower():
                    procstat = 'error'
                    sleepmore = 1
                else:
                    procstat = 'Unknown'
                    print('*ERR*[{0:d}] ... log content follows ...'.format(wget_num))
                    print('{0:s}'.format(status))
                    sleepmore = 1

                print('\tStatus[{0:d}]: {1:s} [{2:s}]'.format(wget_num, procstat, rinex_file))

                if sleepmore:
                    print('\t[sleep {0:d} sec]'.format(sleepsec))
                    time.sleep(sleepsec)
            # Re-wget!
            else:
                print('=> wget[{0:d}]: "Status.txt" *NOT* found! Wget again!'.format(wget_num))

        # ---------------------------------
        # Get result file 'full_output.zip'
        # ---------------------------------
        if not error:
            result_name = 'full_output.zip'
            if os.path.isfile(result_name):
                os.remove(result_name)
            print('=> Get results file: {0:s}'.format(result_name))

            # Iterate!
            # --------
            for wget_num in range(wget_max):
                command = 'wget {0:s} -O {1:s}  "http://webapp.geod.nrcan.gc.ca/CSRS-PPP/service/results/file?id={2:s}"'.format(wget_options, result_name, keyid)
                if debug:
                    print('# Iter[{0:d}] ... {1:s}'.format(wget_num, command))

                # wget
                log = Popen(shlex.split(command), stdout=PIPE, shell=True)
                output = log.communicate()
                output = output[0].decode('utf-8')
                if output and debug:
                    print('log[{0:d}]: {1:s}'.format(wget_num, log))

                if os.path.isfile(result_name):
                    print('=> Okay[{0:d}]: Got file "{1:s}" ... Moved to {2:s} ... if OK!'.format(wget_num, result_name, name + '_' + result_name))

                    # Check zip integrity
                    # command = 'unzip -t %s  2>&1' % result_name
                    command = 'unzip -t {0:s}'.format(result_name)
                    #import pdb; pdb.set_trace()
                    if debug:
                        print('# {0:s}'.format(command))
                    log = Popen(shlex.split(command), stdout=PIPE)
                    output = log.communicate()
                    output = output[0].decode('utf-8')

                    # if 'No errors detected' in log:
                    if 'No errors detected' in output:
                        print('=> Integrity[{0:d}]: OK.'.format(wget_num))
                        os.rename(result_name, name + '_' + result_name)
                        result_name = name + '_' + result_name

                        # Extract sum and pdf
                        # -------------------
                        # command = 'unzip -Z %s 2>&1' % result_name
                        command = 'unzip -Z {0:s}'.format(result_name)
                        log = Popen(shlex.split(command), stdout=PIPE)
                        output = log.communicate()
                        # only need the first index of tuple; decode bytes to utf-8 encoded string
                        output = output[0].decode('utf-8')

                        if output:
                            output_list = output.split('\n')
                            for line in output_list:
                                if 'sum' in line or 'pdf' in line or 'pos' in line:
                                    fields = line.split(' ')
                                    extract_name = fields[-1]
                                    print('\textracting ... {0:s}'.format(extract_name))
                                    # command = 'unzip -xoq %s %s  2>&1' % (result_name, extract_name)
                                    command = 'unzip -xoq {0:s} {1:s}'.format(result_name, extract_name)
                                    log = Popen(shlex.split(command), stdout=PIPE)
                                    output = log.communicate()
                                    output = output[0].decode('utf-8')
                                    if output:
                                        print('\t{0:s}'.format(output))
                            sys.exit()
                    else:
                        print('=> Integrity[{0:d}]: ERR! Log follows...'.format(wget_num))
                        print('{0:s}'.format(log))
                        print('=> Will Re-wget ...')
                        continue  # re-wget!
                else:
                    print('** Error: File "$result_name" *NOT* found!')
                    print('=> Will Re-wget ...')
                    continue  # re-wget!

            # Max wget reached?
            # -----------------
            print('=> Max number of requests [{0:d}] exceeded!'.format(wget_max))
            print('=> RNX: {0:s} [keyid: {1:s}]'.format(rinex_name, keyid))
            print('=> NEXT file!')
            error = 1
            sys.exit(error)
        else:
            print('=> NO results! An error occurred while processing!!!')
            print('=> RNX: {0:s} [keyid: {1:s}]'.format(rinex_name, keyid))
            error = 1
            sys.exit(error)

    # Problems while doing the 'request'
    # ----------------------------------
    # Re-Submit!
    else:
        print('=> Hash{_content} does *NOT* exist!')
        print('=> Re-Submit ...')
        continue

# if it gets here => Problems ... NEXT file!
# ------------------------------------------
print('=> Max number of requests [{0:d}] exceeded! [{1:s}]'.format(request_max, rinex_name))
print('=> Next file ...')
sys.exit(1)
