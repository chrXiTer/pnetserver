# 一个基于ovs的docker 组网方案用使用的命令
import json
import random

from flask import jsonify
from flask import request, abort
from appdc.web import web

from appdc.ovsnew.tool import call_prog, call_popen, ovs_vsctl,  ovn_nbctl

OVN_BRIDGE = "br-int"
OVN_NB = ""



@web.route('/Plugin.Activate', methods=['POST'])
def plugin_activate():
    print('/Plugin.Activate')
    return jsonify({"Implements": ["NetworkDriver"]})

@web.route('/NetworkDriver.GetCapabilities', methods=['POST'])
def get_capability():
    print('/NetworkDriver.GetCapabilities')
    return jsonify({"Scope": "global"})

@web.route('/NetworkDriver.DiscoverNew', methods=['POST'])
def new_discovery():
    print('/NetworkDriver.DiscoverNew')
    return jsonify({})

@web.route('/NetworkDriver.DiscoverDelete', methods=['POST'])
def delete_discovery():
    print('/NetworkDriver.DiscoverDelete')
    return jsonify({})

@web.route('/NetworkDriver.CreateNetwork', methods=['POST'])
def create_network():
    print('/NetworkDriver.CreateNetwork')
    if not request.data:
        abort(400)
    print(request.data)
    data = json.loads(request.data)
    network = data.get("NetworkID", "")
    if not network:
        abort(400)
    ipv4_data = data.get("IPv4Data", "")
    if not ipv4_data:
        error = "create_network: No ipv4 subnet provided"
        return jsonify({'Err': error})

    subnet = ipv4_data[0].get("Pool", "")
    if not subnet:
        error = "create_network: no subnet in ipv4 data from libnetwork"
        return jsonify({'Err': error})
    gateway_ip = ipv4_data[0].get("Gateway", "").rsplit('/', 1)[0]
    if not gateway_ip:
        error = "create_network: no gateway in ipv4 data from libnetwork"
        return jsonify({'Err': error})
    return jsonify({})

@web.route('/NetworkDriver.DeleteNetwork', methods=['POST'])
def delete_network():
    print('/NetworkDriver.DeleteNetwork')
    if not request.data:
        abort(400)
    data = json.loads(request.data)
    print(request.data)
    nid = data.get("NetworkID", "")
    if not nid:
        abort(400)
    return jsonify({})

@web.route('/NetworkDriver.CreateEndpoint', methods=['POST'])
def create_endpoint():
    print('/NetworkDriver.CreateEndpoint')
    if not request.data:
        abort(400)
    print(request.data)
    data = json.loads(request.data)
    nid = data.get("NetworkID", "")
    if not nid:
        abort(400)

    eid = data.get("EndpointID", "")
    if not eid:
        abort(400)

    interface = data.get("Interface", "")
    if not interface:
        error = "create_endpoint: no interfaces structure supplied by " \
                "libnetwork"
        return jsonify({'Err': error})

    ip_address_and_mask = interface.get("Address", "")
    if not ip_address_and_mask:
        error = "create_endpoint: ip address not provided by libnetwork"
        return jsonify({'Err': error})

    ip_address = ip_address_and_mask.rsplit('/', 1)[0]
    mac_address_input = interface.get("MacAddress", "")
    mac_address_output = ""

    

    if not mac_address_input:
        mac_address = "02:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255),
                                                       random.randint(0, 255),
                                                       random.randint(0, 255),
                                                       random.randint(0, 255),
                                                       random.randint(0, 255))
    else:
        mac_address = mac_address_input

    # Only return a mac address if one did not come as request.
    mac_address_output = ""
    if not mac_address_input:
        mac_address_output = mac_address

    return jsonify({"Interface": {
                                    "Address": "",
                                    "AddressIPv6": "",
                                    "MacAddress": mac_address_output
                                    }})

def get_lsp_addresses(eid):
    pass
    '''
    ret = ovn_nbctl("--if-exists", "get", "Logical_Switch_Port", eid,
                    "addresses")
    if not ret:
        error = "endpoint not found in OVN database"
        return (None, None, error)
    addresses = ast.literal_eval(ret)
    if len(addresses) == 0:
        error = "unexpected return while fetching addresses"
        return (None, None, error)
    (mac_address, ip_address) = addresses[0].split()
    return (mac_address, ip_address, None)
    '''


@web.route('/NetworkDriver.EndpointOperInfo', methods=['POST'])
def show_endpoint():
    print('/NetworkDriver.EndpointOperInfo')
    if not request.data:
        abort(400)
    data = json.loads(request.data)
    nid = data.get("NetworkID", "")
    if not nid:
        abort(400)
    eid = data.get("EndpointID", "")
    if not eid:
        abort(400)
    try:
        (mac_address, ip_address, error) = get_lsp_addresses(eid)
        if error:
            jsonify({'Err': error})
    except Exception as e:
        error = "show_endpoint: get Logical_Switch_Port addresses. (%s)" \
                % (str(e))
        return jsonify({'Err': error})

    veth_outside = eid[0:15]
    return jsonify({"Value": {"ip_address": ip_address,
                              "mac_address": mac_address,
                              "veth_outside": veth_outside
                              }})

@web.route('/NetworkDriver.DeleteEndpoint', methods=['POST'])
def delete_endpoint():
    print('/NetworkDriver.DeleteEndpoint')
    if not request.data:
        abort(400)
    data = json.loads(request.data)
    nid = data.get("NetworkID", "")
    if not nid:
        abort(400)
    eid = data.get("EndpointID", "")
    if not eid:
        abort(400)
    return jsonify({})

@web.route('/NetworkDriver.Join', methods=['POST'])
def network_join():
    print('/NetworkDriver.Join')
    if not request.data:
        abort(400)

    data = json.loads(request.data)

    nid = data.get("NetworkID", "")
    if not nid:
        abort(400)

    eid = data.get("EndpointID", "")
    if not eid:
        abort(400)

    sboxkey = data.get("SandboxKey", "")
    if not sboxkey:
        abort(400)

    # sboxkey is of the form: /var/run/docker/netns/CONTAINER_ID
    vm_id = sboxkey.rsplit('/')[-1]
    '''
    try:
        (mac_address, ip_address, error) = get_lsp_addresses(eid)
        if error:
            jsonify({'Err': error})
    except Exception as e:
        error = "network_join: %s" % (str(e))
        return jsonify({'Err': error})
    '''
    veth_outside = eid[0:15]
    veth_inside = eid[0:13] + "_c"
    command = "ip link add %s type veth peer name %s" \
              % (veth_inside, veth_outside)
    '''
    try:
        call_popen(shlex.split(command))
    except Exception as e:
        error = "network_join: failed to create veth pair (%s)" % (str(e))
        return jsonify({'Err': error})

    command = "ip link set dev %s address %s" \
              % (veth_inside, mac_address)


    try:
        call_popen(shlex.split(command))
    except Exception as e:
        error = "network_join: failed to set veth mac address (%s)" % (str(e))
        return jsonify({'Err': error})
    '''

    command = "ip link set %s up" % (veth_outside)

    '''
    try:
        call_popen(shlex.split(command))
    except Exception as e:
        error = "network_join: failed to up the veth interface (%s)" % (str(e))
        return jsonify({'Err': error})


    try:
        ovs_vsctl("add-port", OVN_BRIDGE, veth_outside)
        ovs_vsctl("set", "interface", veth_outside,
                  "external_ids:attached-mac=" + mac_address,
                  "external_ids:iface-id=" + eid,
                  "external_ids:vm-id=" + vm_id,
                  "external_ids:iface-status=active")
    except Exception as e:
        error = "network_join: failed to create a port (%s)" % (str(e))
        return jsonify({'Err': error})
    '''

    return jsonify({"InterfaceName": {
                                        "SrcName": veth_inside,
                                        "DstPrefix": "eth"
                                     },
                    "Gateway": "",
                    "GatewayIPv6": ""})


@web.route('/NetworkDriver.Leave', methods=['POST'])
def network_leave():
    print('/NetworkDriver.Leave')
    if not request.data:
        abort(400)

    data = json.loads(request.data)

    nid = data.get("NetworkID", "")
    if not nid:
        abort(400)

    eid = data.get("EndpointID", "")
    if not eid:
        abort(400)

    veth_outside = eid[0:15]
    command = "ip link delete %s" % (veth_outside)
    return jsonify({})

