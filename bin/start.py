#!/usr/bin/env python
# -*-python-*-

import os
import sys
import logging
import subprocess
import signal
import time
import shutil

# please rewrite me in go (so it can be cross-compiled) ... maybe?

if __name__ == '__main__':

    import optparse
    opt_parser = optparse.OptionParser()

    opt_parser.add_option('-d', '--data', dest='data', action='store', default=None, help='The path to your Who\'s On First data')
    opt_parser.add_option('-f', '--fetch', dest='fetch', action='store_true', default=None, help='Fetch and store data store in the meta files you want to index')
    opt_parser.add_option('-s', '--source', dest='source', action='store', default='https://whosonfirst.mapzen.com/data/', help='Where to pre-fetch data from (default is the root WOF data server)')
    opt_parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Be chatty (default is false)')

    # things you probably don't need to worry about (but some do)

    opt_parser.add_option('--pip-host', dest='pip_host', action='store', default='localhost', help='The host to run the WOF point-in-polygon server on (default is localhost)')
    opt_parser.add_option('--pip-port', dest='pip_port', action='store', default='8080', help='The port to run the WOF point-in-polygon server on (default is 8080)')
    opt_parser.add_option('--data-host', dest='data_host', action='store', default='localhost', help='The host to run the WOF data server on (default is localhost)')
    opt_parser.add_option('--data-port', dest='data_port', action='store', default='9999', help='The port to run the WOF data server on (default is 9999)')
    opt_parser.add_option('--www-host', dest='www_host', action='store', default='localhost', help='The host to run the WOF web server on (default is localhost)')
    opt_parser.add_option('--www-port', dest='www_port', action='store', default='8001', help='The port to run the WOF web server on (default is localhost)')

    options, args = opt_parser.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Make sure we have something to do

    if len(args) == 0:
        logging.error("you forgot to specify any meta files to load")
        sys.exit()

    # Paths

    whatami = sys.platform

    whoami = os.path.abspath(sys.argv[0])
    bin = os.path.dirname(whoami)
    root = os.path.dirname(bin)

    bin = os.path.join(root, "bin")
    www = os.path.join(root, "www")

    # Ensure config file

    js = os.path.join(www, "javascript")
    cfg = os.path.join(js, "mapzen.whosonfirst.config.js")

    if not os.path.exists(cfg):

        example = cfg + ".example"
        shutil.copy(example, cfg)

        if not os.path.exists(cfg):

            logging.error("failed to copy %s to %s!" % (example, cfg))
            sys.exit()

    # Figure out where binaries live

    if whatami == 'darwin':
        bin = os.path.join(bin, "osx")
    elif whatami == 'windows':
        bin = os.path.join(bin, "win32")
    elif whatami == 'linux' or whatami == 'linux2':	# what is linux2???
        bin = os.path.join(bin, "linux")        
    else:
        logging.error("unknown or unsupported platform: %s" % whatami)
        sys.exit()

    pip_server = os.path.join(bin, "wof-pip-server")
    file_server = os.path.join(bin, "wof-fileserver")
    clone_tool = os.path.join(bin, "wof-clone-metafiles")

    # Do I need to pre-fetch any data?

    if options.fetch:

        logging.info("pre-fetching %s" % " ".join(args))

        dest = os.path.abspath(options.data)

        cmd = [clone_tool, "-dest", dest, "-source", options.source, "-procs", 24]
        cmd.extend(args)

        subprocess.check_call(cmd)

    # Start the various background servers

    # pip_cmd = [pip_server, "-cors", "-host", options.pip_host, "-port", options.pip_port, "-data", options.data]

    pip_cmd = [pip_server, "-cors", "-port", options.pip_port, "-data", options.data]
    pip_cmd.extend(args)

    # data_cmd = [file_server, "-cors", "-host", options.data_host, "-port", options.data_port, "-path", options.data]
    # www_cmd = [file_server, "-host", options.www_host, "-port", options.www_port, "-path", www]

    data_cmd = [file_server, "-cors", "-port", options.data_port, "-path", options.data]
    www_cmd = [file_server, "-port", options.www_port, "-path", www]

    logging.debug(" ".join(pip_cmd))
    logging.debug(" ".join(data_cmd))
    logging.debug(" ".join(www_cmd))

    pip = subprocess.Popen(pip_cmd)
    data = subprocess.Popen(data_cmd)
    www = subprocess.Popen(www_cmd)

    # Watch for ctrl-C

    def signal_handler(signal, frame):

        pip.terminate()
        data.terminate()
        www.terminate()

        raise Exception, "all done"

    signal.signal(signal.SIGINT, signal_handler)

    # Spin spin sping...

    try:
        while True:
            time.sleep(.5)
    except Exception, e:
        pass

    logging.info("all done")
    sys.exit()
    
