import argparse
import ast
import atexit
import json
import os
import random
import re
import shlex
import subprocess
import sys

import ovs.dirs
import ovs.util
import ovs.daemon
import ovs.vlog

from flask import Flask, jsonify
from flask import request, abort

vlog = ovs.vlog.Vlog("ovn-docker-overlay-driver")

OVN_BRIDGE = "br-int"
OVN_NB = ""
PLUGIN_DIR = "/etc/docker/plugins"
PLUGIN_FILE = "/etc/docker/plugins/openvswitch.spec"


def ovn_nbctl(*args):
    args_list = list(args)
    database_option = "%s=%s" % ("--db", OVN_NB)
    args_list.insert(0, database_option)
    return call_prog("ovn-nbctl", args_list)

def call_popen(cmd):
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = child.communicate()
    if child.returncode:
        raise RuntimeError("Fatal error executing %s" % (cmd))
    if len(output) == 0 or output[0] == None:
        output = ""
    else:
        output = output[0].strip()
    return output


def call_prog(prog, args_list):
    cmd = [prog, "--timeout=5", "-vconsole:off"] + args_list
    #return call_popen(cmd)


def ovs_vsctl(*args):
    pass
    #return call_prog("ovs-vsctl", list(args))


def cleanup():
    if os.path.isfile(PLUGIN_FILE):
        os.remove(PLUGIN_FILE)

def ovn_init_overlay():
    '''
    br_list = ovs_vsctl("list-br").split()
    if OVN_BRIDGE not in br_list:
        ovs_vsctl("--", "--may-exist", "add-br", OVN_BRIDGE,
                  "--", "set", "bridge", OVN_BRIDGE,
                  "external_ids:bridge-id=" + OVN_BRIDGE,
                  "other-config:disable-in-band=true", "fail-mode=secure")

    global OVN_NB
    OVN_NB = ovs_vsctl("get", "Open_vSwitch", ".",
                           "external_ids:ovn-nb").strip('"')
    if not OVN_NB:
        sys.exit("OVN central database's ip address not set")

    ovs_vsctl("set", "open_vswitch", ".",
              "external_ids:ovn-bridge=" + OVN_BRIDGE)
    '''

def prepare():
    '''
    parser = argparse.ArgumentParser()

    ovs.vlog.add_args(parser)
    ovs.daemon.add_args(parser)
    args = parser.parse_args()
    ovs.vlog.handle_args(args)
    ovs.daemon.handle_args(args)
    '''
    ovn_init_overlay()

    if not os.path.isdir(PLUGIN_DIR):
        os.makedirs(PLUGIN_DIR)

    ovs.daemon.daemonize()
    try:
        fo = open(PLUGIN_FILE, "w")
        fo.write("tcp://0.0.0.0:8100")
        fo.close()
    except Exception as e:
        ovs.util.ovs_fatal(0, "Failed to write to spec file (%s)" % str(e),
                           vlog)

    atexit.register(cleanup)