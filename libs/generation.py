#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2016 Zomboided
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#    Generate the template and location files based on whatever info 
#    available.  Minimal error coding as it's only to run once (infrequently)
#    and not by the end user.


import xbmc
import xbmcgui
import xbmcvfs
import glob
import string
from libs.utility import debugTrace, errorTrace, infoTrace, newPrint
from libs.platform import getAddonPath, getUserDataPath, fakeConnection
from libs.common import getFriendlyProfileName

def generateAll():
    infoTrace("generation.py", "Generating Location files")
    generatePP()
    return
    generateLiquidVPN()
    generateVPNac()
    generateNordVPN()
    generateCyberGhost()
    generateVPNUnlim()
    generateVyprVPN()
    generateExpressVPN()
    generatePureVPN()
    generatePIA()
    generateNordVPN()
    generateSmartDNSProxy()
    generateIVPN()
    generateCelo()
    generateHMA()
    generateRA4W()
    generateVPNSecure()
    generateIPVanish()
    generateHideIPVPN()
    generateExpressVPN()
    generateSecureVPN()
    generateLimeVPN()
    generateSecureVPN()
    generateNordVPN()
    generateproXPN()
    generateWindscribe()
    generateWiTopia()
    generateVPNht()
    generateTotalVPN()    
    generateSaferVPN()
    generateBTGuard()
    generateHideMe()
    generateHideIPVPN()
    generateVyprVPN()
    generateTorGuard()
    generateibVPN()
    generateAirVPN()
    generatePIA()
    generatetigerVPN()   
    generateIPVanish()    

def getLocations(vpn_provider, path_ext):
    if path_ext == "":
        location_path = "/LOCATIONS.txt"
    else:
        location_path = "/LOCATIONS " + path_ext + ".txt"
    return open(getAddonPath(True, vpn_provider + location_path), 'w')


def getProfileList(vpn_provider):
    path = getUserDataPath("providers/" + vpn_provider + "/*.ovpn")
    return glob.glob(path)      

    
def generateVPNac():
    # Data is stored as a bunch of ovpn files
    # File name has location.  File has the servers
    profiles = getProfileList("VPN.ac")
    location_file = getLocations("VPN.ac", "")
    for profile in profiles:
        geo = profile[profile.rfind("\\")+1:profile.index(".ovpn")]
        if "tcp" in geo:
            proto = "tcp"
        else:
            proto = "udp"
        geo = geo.replace("-aes128-tcp", "")
        geo = geo.replace("-aes128-udp", "")
        geo = geo.replace("_", " ")
        geo = geo.title()
        geo = geo.replace("Us-East ", "US-East ")
        geo = geo.replace("Us-West ", "US-West ")
        geo = geo.replace("Us-Central ", "US-Central ")
        geo = geo.replace("Uk ", "UK ")
        geo = geo.replace("-2", " 2")
        geo = geo.replace("-3", " 3")
        servers = ""
        ports = ""
        writeline = ""
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split()
                proto = proto.lower()
                if not servers == "" : servers = servers + " "
                servers = servers + server
                if not ports == "" : ports = ports + " "
                ports = ports + port
        output_line = geo + " (" + proto.upper() + ")," + servers + "," + proto + "," + ports + "\n" 
        location_file.write(output_line)
    location_file.close()   
    
    
    
    

def generateSmartDNSProxy():
    # Data is stored as a bunch of ovpn files
    profiles = getProfileList("SmartDNSProxy")
    location_file = getLocations("SmartDNSProxy", "")
    for profile in profiles:
        geo = profile[profile.index("SmartDNSProxy\\")+14:]
        geo = geo.replace(".ovpn", "")
        udp_found = False
        tcp_found = False
        smart_found = False
        if "UDP" in profile: 
            udp_found = True
            proto = "udp"
            geo = geo.replace("UDP1194", "")            
        if "TCP" in profile: 
            tcp_found = True
            proto = "tcp"
            geo = geo.replace("TCP443", "")
        if "SMART" in profile:
            smart_found = True
            geo = geo.replace("SMART", "")
        geo = geo.replace("__", "_")
        geo = geo.replace("_", " ")
        geo = geo.replace("-", " - ")
        if udp_found:
            if smart_found:
                geo = geo + ("(UDP Smart)")
            else:
                geo = geo + " (UDP)"
        if tcp_found:
            if smart_found:
                geo = geo + " (TCP Smart)"
            else:
                geo = geo + " (TCP)"
        geo = geo.replace("  ", " ")
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split()             
        output_line = geo + "," + server + "," + proto + "," + port + "\n"
        location_file.write(output_line)
    location_file.close()
    
    
def generateWindscribe():
    # Data is stored in a flat text file
    # It's just a list of server names
    location_file = getLocations("Windscribe", "")
    source_file = open(getUserDataPath("providers/Windscribe/Servers.txt"), 'r')
    source = source_file.readlines()
    source_file.close()
    for line in source:
        line = line.strip(" \t\n\r")
        server = line
        geo = line.replace(".windscribe.com", "")
        if "-" in geo:
            geo, rest = geo.split("-")
            rest = " " + string.capwords(rest)
        else:
            rest = ""
        geo = resolveCountry(geo.upper()) + rest
        output_line_udp = geo + " (UDP)," + server + "," + "udp,443"  + "\n"
        output_line_tcp = geo + " (TCP)," + server + "," + "tcp,443" + "\n"
        location_file.write(output_line_udp)
        location_file.write(output_line_tcp)
    location_file.close()

    
def generateRA4W():
    # Data is stored as a bunch of OVPN files
    # File name has location, file has server and port
    profiles = getProfileList("RA4WVPN")
    location_file = getLocations("RA4WVPN", "")
    for profile in profiles:
        geo = profile[profile.rfind("\\")+1:profile.index(".ovpn")]
        geo = geo.replace("ra4wvpn-", "")
        geo = geo.replace("-tcp443", "")
        geo = geo.replace("washingtondc", "Washington DC")
        geo = geo.replace("hongkong", "Hong Kong")
        geo = geo.replace("losangeles", "Los Angeles")
        geo = geo.replace("stpetersburg", "St Petersburg")
        geo = geo.replace("panamacity", "Panama City")
        geo = resolveCountry(geo[0:2].upper()) + " - " + string.capwords(geo[3:])
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split()
        if "-tcp" in profile:
            geo = geo + " (TCP)"
            output_line = geo + "," + server + "," + "tcp," + port + "\n"
        else:
            geo = geo + " (UDP)"
            output_line = geo + "," + server + "," + "udp," + port + "\n"
        location_file.write(output_line)
    location_file.close()     
    

def generateVPNSecure():
    # Data is stored as a bunch of OVPN files
    # File name has location, file has server and port
    profiles = getProfileList("VPNSecure")
    location_file = getLocations("VPNSecure", "")
    for profile in profiles:
        geo = profile[profile.rfind("\\")+1:profile.index(".ovpn")][0:3]
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split()
        geo = resolveCountry(geo[0:2].upper()) + " " + geo[2:3]
        if "ustream" in profile:
            geo = "Ustream 1"            
        if "-TCP" in profile:
            geo = geo + " (TCP)"
            output_line = geo + "," + server + "," + "tcp," + port + "\n"
        else:
            geo = geo + " (UDP)"
            output_line = geo + "," + server + "," + "udp," + port + "\n"
        location_file.write(output_line)
    location_file.close()    

    
def generateSecureVPN():
    # Can't use a template as SecureVPN use multiple everything. 
    # Copy the file to the target directory and strip it of user keys
    existing_profiles = glob.glob(getUserDataPath("providers/SecureVPN" + "/*.ovpn"))
    for connection in existing_profiles:
        xbmcvfs.delete(connection)
    # Get the list from the provider data directory
    profiles = getProfileList("SecureVPN")
    destination_path = getAddonPath(True, "SecureVPN" + "/")   
    for profile in profiles:
        shortname = profile[profile.index("SecureVPN")+10:]
        shortname = shortname[:shortname.index(".")]
        proto = "(UDP)"
        filename = shortname + " " + proto + ".ovpn"
        profile_file = open(profile, 'r')
        output_file = open(destination_path + filename, 'w')
        profile_contents = profile_file.readlines()
        profile_file.close()
        output = ""
        i = 0
        write = True;
        for line in profile_contents:
            line = line.strip(' \t\n\r')
            if not (line == "" or line.startswith("#")) :
                if "<key>" in line or "<cert>" in line: write = False
                if "</key>" in line: 
                    write = True
                    line = "key #USERKEY"
                if "</cert>" in line:
                    write = True
                    line = "cert #USERCERT"
                if write : output_file.write(line + "\n")
            i = i + 1    
        output_file.close()
        
    
def generateIVPN():
    # Data is stored as a bunch of OVPN files
    # File name has location, file has server and port
    profiles = getProfileList("IVPN")
    location_file = getLocations("IVPN", "")
    for profile in profiles:
        geo = profile[profile.rfind("\\")+1:profile.index(".ovpn")]
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split()
            if line.startswith("verify-x509-name"):
                _, prefix, _ = line.split()
        if "-TCP" in geo:
            geo = geo.replace("-TCP", " (TCP)")
            output_line = geo + "," + server + "," + "tcp-client," + port + ",#USER1=" + prefix + "\n"
        else:
            geo = geo + " (UDP)"
            output_line = geo + "," + server + "," + "udp," + port + ",#USER1=" + prefix + "\n"
        location_file.write(output_line)
    location_file.close()
    
def generateproXPN():
    # Data is stored in a flat text file
    # Location, tab, server - free locations are marked with a leading *
    location_file_full = getLocations("proXPN", "Full Account")
    location_file_free = getLocations("proXPN", "Free Account")
    source_file = open(getUserDataPath("providers/proXPN/Servers.txt"), 'r')
    source = source_file.readlines()
    source_file.close()
    for line in source:
        line = line.strip(" \t\n\r")
        if not ("UDP" in line or "TCP" in line):
            geo = line.strip(" \t\n\r")
            geo = geo.replace(",", " -")
        else:
            if "Free" in geo:
                server = line[line.index("IP:")+3:]
            else:
                server = line[line.index("  "):line.index(".com")+4]
            server = server.strip(" \t\n\r")
            if "UDP" in line:    
                output_line = geo + " (UDP)," + server + "," + "udp,443" + "\n"
            if "TCP" in line:
                output_line = geo + " (TCP)," + server + "," + "tcp,443" + "\n"
            if "Free" in geo:
                location_file_free.write(output_line)
            else:
                location_file_full.write(output_line)
    location_file_full.close()
    location_file_free.close()    
    
def generateWiTopia():
    # Data is stored in a flat text file
    # City name followed by server name, or just server name (starts with vpn.)
    location_file = getLocations("WiTopia", "")
    source_file = open(getUserDataPath("providers/WiTopia/Servers.txt"), 'r')
    source = source_file.readlines()
    source_file.close()
    city = ""
    cont = ""
    for line in source:
        line = line.strip(" \t\n\r")
        if not line.startswith("vpn."):
            if line.startswith("-"):
                cont = line.replace("-", "")
                if not cont == "": cont = cont + " - "
            else:
                city = line
        else:
            if city == "":
                city = line.replace("vpn.","").replace(".witopia.net","")
                city = string.capwords(city)
            geo = cont + city
            server = line
            output_line_udp = geo + " (UDP)," + server + "," + "udp,1194"  + "\n"
            city = ""
            location_file.write(output_line_udp)
    location_file.close()
    
    
def generateTotalVPN():
    # Data is stored in a flat text file
    # Location, tab, server - free locations are marked with a leading *
    location_file_full = getLocations("TotalVPN", "Full Account")
    location_file_free = getLocations("TotalVPN", "Free Account")
    source_file = open(getUserDataPath("providers/TotalVPN/Servers.txt"), 'r')
    source = source_file.readlines()
    source_file.close()
    for line in source:
        line = line.strip(" \t\n\r")
        geo, server = line.split("\t")
        geo = geo.strip(" *\t\n\r")
        geo = geo.replace(",", " -")
        output_line_udp = geo + " (UDP)," + server + "," + "udp,1194"  + "\n"
        output_line_tcp = geo + " (TCP)," + server + "," + "tcp,443" + "\n"
        location_file_full.write(output_line_udp)
        location_file_full.write(output_line_tcp)
        if "*" in line:
            location_file_free.write(output_line_udp)
            location_file_free.write(output_line_tcp)
    location_file_full.close()
    location_file_free.close()
    
    
def generateCelo():
    # Data is stored as a bunch of ovpn files
    # File name has location.  File has the server
    profiles = getProfileList("Celo")
    location_file = getLocations("Celo", "")
    for profile in profiles:
        geo = profile[profile.rfind("\\")+1:profile.index(".ovpn")]
        geo = geo.replace("sw", "se")
        geo = geo.replace(".celo.net", "")
        geo = geo = resolveCountry(geo[0:2].upper()) + " " + geo[2:3]
        geo_key = (geo + "_ta.key").replace(" ", "_")
        geo_cert = (geo + "_ca.crt").replace(" ", "_")
        geo_key_file = open(getAddonPath(True, "Celo/" + geo_key), 'w')
        geo_cert_file = open(getAddonPath(True, "Celo/" + geo_cert), 'w')
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        servers_udp = ""
        servers_tcp = ""
        ports_udp = ""
        ports_tcp = ""
        writeline = ""
        for line in lines:
            if line.startswith("remote "):
                _, server, port, proto = line.split()
                proto = proto.lower()
                if proto == "udp":
                    if not servers_udp == "" : servers_udp = servers_udp + " "
                    servers_udp = servers_udp + server
                    if not ports_udp == "" : ports_udp = ports_udp + " "
                    ports_udp = ports_udp + port
                if proto == "tcp":
                    if not servers_tcp == "" : servers_tcp = servers_tcp + " "
                    servers_tcp = servers_tcp + server
                    if not ports_tcp == "" : ports_tcp = ports_tcp + " "
                    ports_tcp = ports_tcp + port
            if writeline == "ca":
                if line.startswith("</ca>"):
                    writeline = ""
                    geo_cert_file.close()
                else:
                    if not line.startswith("#"): geo_cert_file.write(line)
            if line.startswith("<ca>"):
                writeline = "ca"
            if writeline == "tls":
                if line.startswith("</tls-auth>"):
                    writeline = ""
                    geo_key_file.close()
                else:
                    if not line.startswith("#"): geo_key_file.write(line)
            if line.startswith("<tls-auth>"):
                writeline = "tls"
            
        output_line_udp = geo + " (UDP)," + servers_udp + "," + "udp," + ports_udp + ",#TLSKEY=" + geo_key + " #CERT=" + geo_cert + "\n" 
        output_line_tcp = geo + " (TCP)," + servers_tcp + "," + "tcp," + ports_tcp + ",#TLSKEY=" + geo_key + " #CERT=" + geo_cert + "\n"         
        location_file.write(output_line_udp)
        location_file.write(output_line_tcp)
    location_file.close()   
    
    
def generateVPNht():
    # Data is stored in a flat text file
    # Location on one line, then server on the next
    location_file_smartdns = getLocations("VPN.ht", "With SmartDNS")
    location_file_without = getLocations("VPN.ht", "Without SmartDNS")
    location_file_all = getLocations("VPN.ht", "All Connections")
    source_file = open(getUserDataPath("providers/VPN.ht/Servers.txt"), 'r')
    source = source_file.readlines()
    source_file.close()
    i = 0
    for line in source:
        if i == 0:
            i = 1
            geo = line.strip(' \t\n\r')
        else:
            i = 0
            server = line.strip(' \t\n\r')
            serverudp = server
            for j in range (1, 7):
                serverudp = serverudp + " " + server
            output_line_udp = geo + " (UDP)," + serverudp + "," + "udp,1194 1195 1196 1197 1198 1199 1200"  + "\n"
            output_line_udp_no = geo + " (UDP SmartDNS)," + serverudp + "," + "udp,1194 1195 1196 1197 1198 1199 1200"  + ",#REMOVE=1\n"
            output_line_tcp_no = geo + " (TCP)," + server + "," + "tcp,443"  + ",#REMOVE=1\n"
            output_line_tcp = geo + " (TCP SmartDNS)," + server + "," + "tcp,443"  + "\n"
            location_file_smartdns.write(output_line_udp)
            location_file_smartdns.write(output_line_tcp)
            location_file_without.write(output_line_udp_no)
            location_file_without.write(output_line_tcp_no)
            location_file_all.write(output_line_udp)
            location_file_all.write(output_line_tcp)
            location_file_all.write(output_line_udp_no)
            location_file_all.write(output_line_tcp_no)
    location_file_smartdns.close()   
    location_file_without.close()
    location_file_all.close()
    
    
def generateSaferVPN():
    # Data is stored as a bunch of ovpn files
    # File name has location.  File has the server
    profiles = getProfileList("SaferVPN")
    location_file = getLocations("SaferVPN", "")
    for profile in profiles:
        geo = profile[profile.index("SaferVPN")+9:]
        geo = geo.replace(".ovpn", "")
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        for line in lines:
            if line.startswith("remote "):
                line = line[:line.index("#")-2]
                _, server, port = line.split()  
        output_line_udp = geo + " (UDP)," + server + "," + "udp,1194" + "\n"
        output_line_tcp = geo + " (TCP)," + server + "," + "tcp,443" + "\n"
        location_file.write(output_line_udp)
        location_file.write(output_line_tcp)
    location_file.close()

    
def generateExpressVPN():
    # Data is stored as a bunch of ovpn files
    profiles = getProfileList("ExpressVPN")
    location_file = getLocations("ExpressVPN", "")
    for profile in profiles:
        geo = profile[profile.index("my_expressvpn_")+14:]
        geo = geo.replace("_"," ")
        geo = geo.replace(" udp", "")
        geo = geo.replace(".ovpn", "")
        geo = string.capwords(geo)
        geo = geo.replace("Uk ", "UK ")
        geo = geo.replace("Usa ", "USA ")
        geo = geo.replace(" Cbd", " CBD")
        geo = geo.replace(" Dc", " DC")
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split()  
        output_line_udp = geo + " (UDP)," + server + "," + "udp,1195" + "\n"
        output_line_tcp = geo + " (TCP)," + server + "," + "tcp-client,443" + ",#REMOVE=1\n"
        location_file.write(output_line_udp)
        location_file.write(output_line_tcp)
    location_file.close()
    
        
def generateBTGuard():
    # Data is stored as a bunch of ovpn files
    # File name has location.  File has the server
    profiles = getProfileList("BTGuard")
    location_file = getLocations("BTGuard", "")
    for profile in profiles:
        if not "TCP" in profile:
            geo = profile[profile.index("BTGuard ")+8:]
            geo = geo.replace("- ","")
            geo = geo.replace("(Fastest)", "Fastest")
            geo = geo.replace(".ovpn", "")
            profile_file = open(profile, 'r')
            lines = profile_file.readlines()
            profile_file.close()
            for line in lines:
                if line.startswith("remote "):
                    _, server, port = line.split()  
            output_line_udp = geo + " (UDP)," + server + "," + "udp,1194" + "\n"
            output_line_tcp = geo + " (TCP)," + server + "," + "tcp,443" + "\n"
            location_file.write(output_line_udp)
            location_file.write(output_line_tcp)
    location_file.close()    
    

def generateLimeVPN():
    # Can't use a template as LimeVPN use server certs. 
    # Copy the file to the target directory and strip it of user keys
    existing_profiles = glob.glob(getAddonPath(True, "LimeVPN" + "/*.ovpn"))
    for connection in existing_profiles:
        xbmcvfs.delete(connection)
    # Get the list from the provider data directory
    profiles = getProfileList("LimeVPN")
    destination_path = getAddonPath(True, "LimeVPN" + "/")   
    for profile in profiles:
        shortname = profile[profile.index("LimeVPN")+8:]
        shortname = shortname.replace("_openvpn_remote_access_l3", "")
        shortname = shortname[:shortname.index(".")]
        shortname = shortname.replace("aus", "au")
        shortname = shortname.replace("sw", "se")
        shortname = shortname.replace("sk", "kr")
        countryname = resolveCountry(shortname[0:2].upper())
        if len(shortname) == 3:
            shortname = " " + shortname[2:3]
        else:
            shortname = ""
        proto = " (UDP)"
        filename = countryname + shortname + proto + ".ovpn"
        profile_file = open(profile, 'r')
        output_file = open(destination_path + filename, 'w')
        profile_contents = profile_file.readlines()
        profile_file.close()
        output = ""
        i = 0
        write = True;
        for line in profile_contents:
            line = line.strip(' \t\n\r')
            if not (line == "" or line.startswith("#")) :
                if "<key>" in line or "<cert>" in line: write = False
                if "</key>" in line: 
                    write = True
                    line = ""
                if "</cert>" in line:
                    write = True
                    line = ""
                if write and not line == "" : 
                    output_file.write(line + "\n")
            i = i + 1    
        output_file.close()   
    
    
def generateHideIPVPN():
    # Data is stored as a bunch of ovpn files
    # File name has the country, but needs translation, files have multiple servers/ports
    profiles = getProfileList("HideIPVPN")
    location_file = getLocations("HideIPVPN", "Full and Trial Account")
    location_file_uk = getLocations("HideIPVPN", "UK VPN")
    location_file_us = getLocations("HideIPVPN", "US VPN")
    location_file_poland = getLocations("HideIPVPN", "Poland VPN")
    for profile in profiles:
        geo = profile[profile.rfind("\\")+1:profile.index(".ovpn")]
        geo = geo.replace(".hideipvpn.com_"," ")
        geo = geo.replace("pl", "Poland ")
        geo = geo.replace("de", "Germany ")
        geo = geo.replace("ca", "Canada ")
        geo = geo.replace("nl", "Netherlands ")
        geo = geo.replace("uk", "United Kingdom ")
        geo = geo.replace("us", "United States ")
        geo = geo.replace("TCP", "(TCP)")
        geo = geo.replace("UDP", "(UDP)")
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        servers = ""
        ports = ""
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split()
                if not servers == "" : servers = servers + " "
                servers = servers + server
                if not ports == "" : ports = ports + " "
                ports = ports + port
            if line.startswith("proto "):
                _, proto = line.split()
        output_line = geo + "," + servers + "," + proto + "," + ports + "\n" 
        location_file.write(output_line)
        if "Kingdom" in geo: location_file_uk.write(output_line)
        if "States" in geo: location_file_us.write(output_line)
        if "Poland" in geo: location_file_poland.write(output_line)
    location_file.close()      
    location_file_uk.close()
    location_file_us.close()
    location_file_poland.close()
    
    
def generateCyberGhost():
    # Data is stored as a bunch of ovpn files
    # File name has location but needs mapping.  File has the server
    profiles = getProfileList("CyberGhost")
    location_file = getLocations("CyberGhost", "Premium and Premium Plus Account")
    for profile in profiles:
        geo = profile[profile.rfind("\\")+1:profile.index(".ovpn")]
        geo = resolveCountry(geo[0:2]) + geo[2:]
        geo = geo.replace("TCP", "(TCP)")
        geo = geo.replace("UDP", "(UDP)")
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        servers = ""
        ports = ""
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split()
                if not servers == "" : servers = servers + " "
                servers = servers + server
                if not ports == "" : ports = ports + " "
                ports = ports + port
            if line.startswith("proto "):
                _, proto = line.split()
        if "(TCP)" in geo : output_line = geo + "," + servers + "," + proto + "," + ports + ",#REMOVE=1 #PINGSPEED=15 #PINGEXIT=90\n"
        if "(UDP)" in geo : output_line = geo + "," + servers + "," + proto + "," + ports + ",#PINGSPEED=5 #PINGEXIT=60\n"
        location_file.write(output_line)
    location_file.close()      

    return


    
def generateTorGuard():
    # Data is stored as a bunch of ovpn files
    # File name has location.  File has the server
    profiles = getProfileList("TorGuard")
    location_file = getLocations("TorGuard", "")
    for profile in profiles:
        geo = profile[profile.rfind("\\")+1:profile.index(".ovpn")]
        geo = geo.replace("TorGuard.","")
        geo = geo.replace(".Stealth.TCP", " Stealth")
        geo = geo.replace(".Stealth.UDP", " Stealth")
        geo = geo.replace("-", " - ")
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        servers = ""
        ports = ""
        proto = ""
        rem_flags = ""
        cipher = False
        remote_server = False
        float = False
        route = False
        remote_random = False
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split()
                if not servers == "" : servers = servers + " "
                servers = servers + server
                if not ports == "" : ports = ports + " "
                ports = ports + port
            if line.startswith("proto "):
                _, proto = line.split() 
            if line.startswith("dev tun"): 
                if line.startswith("dev tun1"):
                    rem_flags = rem_flags + "2"
                else:
                    rem_flags = rem_flags + "1"
            if line.startswith("cipher AES-256-CBC"):
                cipher = True
            if line.startswith("remote-cert-tls server"):
                remote_server = True
            if line.startswith("float"):
                float = True
            if line.startswith("route-delay"):
                route = True
            if line.startswith("remote-random"):
                remote_random = True
        if not cipher: rem_flags = rem_flags + "3"
        if not remote_server: rem_flags = rem_flags + "4"
        if not float: rem_flags = rem_flags + "5"
        if not route: rem_flags = rem_flags + "6"
        if not remote_random: rem_flags = rem_flags + "7"
        output_line = geo + " (" + proto.upper() + ")," + servers + "," + proto + "," + ports + ",#REMOVE=" + rem_flags + "\n"
        location_file.write(output_line)
    location_file.close()      
    
    
def generatePP():
    # Data is stored as a bunch of ovpn files
    # File name has location.  File has the server
    profiles = getProfileList("PerfectPrivacy")
    location_file = getLocations("PerfectPrivacy", "")
    for profile in profiles:
        geo = profile[profile.rfind("\\")+1:profile.index(".ovpn")]
        geo = geo.replace("TelAviv", "Tel Aviv")
        geo = geo.replace("Hongkong", "Hong Kong")
        geo = geo.replace("NewYork", "New York")
        geo_key = geo + "_ta.key"
        if not xbmcvfs.exists(getAddonPath(True, "PerfectPrivacy/" + geo_key)):
            geo = "****ERROR****"
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        servers = ""
        ports = ""
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split()
                if not servers == "" : servers = servers + " "
                servers = servers + server
                if not ports == "" : ports = ports + " "
                ports = ports + port
        output_line = geo + " (UDP)," + servers + "," + "udp," + ports + ",#TLSKEY=" + geo_key + "\n" 
        location_file.write(output_line)
    location_file.close()      
    

def generateHideMe():
    # Data is stored in ovpn files with location info in Servers.txt
    location_file = getLocations("HideMe", "")
    profiles = getProfileList("HideMe")
    for profile in profiles:
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        geo = profile[profile.rfind("\\")+1:profile.index(".ovpn")]
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split()
            if line.startswith("proto "):
                _, proto = line.split()                
        output_line = geo + " (" + proto.upper() + ")," + server + "," + proto + "," + port + "\n"
        location_file.write(output_line)
    location_file.close()
    

def generateVPNUnlim():
    # Data is stored in ovpn files with location info in Servers.txt
    location_file = getLocations("VPNUnlimited", "")
    profiles = getProfileList("VPNUnlimited")
    source_file = open(getUserDataPath("providers/VPNUnlimited/Servers.txt"), 'r')
    servers = source_file.readlines()
    source_file.close()
    i = 0
    for profile in profiles:
        partial = profile[profile.index(".com_")+5:]
        partial = partial[:partial.index("_")]
        profiles[i] = partial
        i += 1
    for entry in servers:    
        geo = entry[:entry.index(",")].strip()
        server = entry[entry.index(",")+1:].strip()
        i = 0
        for profile in profiles:
            if profile in server:
                profiles[i] = ""
            i += 1
        output_line_udp = geo + " (UDP)," + server + ",udp,443\n"
        output_line_tcp = geo + " (TCP)," + server + ",tcp,80\n"
        location_file.write(output_line_udp)
        location_file.write(output_line_tcp) 
    location_file.close()
    for profile in profiles:
        if not profile == "":
            newPrint(profile + " is missing")
        

    
def generateAirVPN():
    # Data is stored in ovpn files
    # File name is AirVPN_Location_rest
    location_file_hosts = getLocations("AirVPN", "DNS Names")
    location_file_ip = getLocations("AirVPN", "IP Addresses")
    directories = ["Resolved", "Hostnames"]
    for directory in directories:
        profiles = getProfileList("AirVPN/" + directory)
        for profile in profiles:
            profile_file = open(profile, 'r')
            lines = profile_file.readlines()
            profile_file.close()
            tokens = (profile[profile.rfind("\\")+1:profile.index(".ovpn")]).split("_")
            geo = tokens[1]
            for line in lines:
                if line.startswith("remote "):
                    _, server, port = line.split()
                if line.startswith("proto "):
                    _, proto = line.split()                
            output_line = geo + " (" + proto.upper() + ")," + server + "," + proto + "," + port + "\n"
            if directory == "Resolved" : location_file_ip.write(output_line)
            if directory == "Hostnames" : location_file_hosts.write(output_line)
    location_file_hosts.close()
    location_file_ip.close()
    
    
def generateLiquidVPN():
    directories = ["Canada", "Netherlands", "Romania", "Singapore", "Sweden", "Switzerland", "United Kingdom", "USA"]
    location_file = getLocations("LiquidVPN", "Connections recommended use with Kodi")
    location_file_all = getLocations("LiquidVPN", "All connections")
    for directory in directories:
        profiles = getProfileList("LiquidVPN/" + directory)
        for profile in profiles:
            profile_file = open(profile, 'r')
            lines = profile_file.readlines()
            profile_file.close()
            server = ""
            tls_auth_flag1 = False
            key_method_flag2 = False
            reneg_sec_flag3 = False
            auth_SHA512_flag4 = False
            remote_random_flag5 = False
            for line in lines:
                if line.startswith("tls-auth") : tls_auth_flag1 = True
                if line.startswith("key-method") : key_method_flag2 = True
                if line.startswith("reneg-sec") : reneg_sec_flag3 = True
                if line.startswith("auth SHA512") : auth_SHA512_flag4 = True
                if line.startswith("remote-random") : remote_random_flag5 = True
                tokens = line.split()
                if len(tokens) > 2:
                    if tokens[0] == "remote" : 
                        if not server == "" : server = server + " "
                        server = server + tokens[1]
            line = profile[profile.rfind("\\")+1:profile.index(".ovpn")]
            if directory == "Netherlands": line = line[2:]
            tokens = line.split()
            geo = directory + " - " + tokens[0] + " " + tokens[2] + " (" + tokens[3] + " " + tokens[4] + ")"
            tokens[3] = tokens[3].lower()
            extra = ""
            if directory == "Romania": extra = ",#CERT=ca_romania.crt "
            flags = ""
            if not tls_auth_flag1 : flags = flags + "1"
            if not key_method_flag2 : flags = flags + "2"
            if not reneg_sec_flag3 : flags = flags + "3"
            if not auth_SHA512_flag4 : flags = flags + "4"
            if not remote_random_flag5 : flags = flags + "5"
            if extra == "" and not flags == "": extra = ","
            if not flags == "":
                extra = extra + "#REMOVE=" + flags
            output_line = geo + "," + server + "," + tokens[3] + "," + tokens[4] + extra + "\n"
            if not tokens[2] == "Modulating" : location_file.write(output_line)
            location_file_all.write(output_line)
    location_file.close()
    

def generateibVPN():
    # Data is stored as a bunch of ovpn files
    # File name has location.  File has the server
    profiles = getProfileList("ibVPN")
    location_file = getLocations("ibVPN", "All Locations")
    location_file_usa = getLocations("ibVPN", "USA and Canada")
    location_file_uk = getLocations("ibVPN", "UK and Ireland")
    location_file_eu = getLocations("ibVPN", "EU")
    usa = ["US", "CA"]
    uk = ["UK", "IE"]
    eu = ["DE", "NL", "FR", "CH", "LU", "RO", "SE", "ES", "IT", "FI", "PL", "AT", "CZ", "HU", "IS", "NO", "BG", "BE", "PT"]
    for profile in profiles:
        geo = profile[profile.index("ibVPN ")+6:]
        geo = geo.replace(".ovpn", "")
        geo = geo.replace("-", " - ")
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        servers = ""
        ports = ""
        for line in lines:
            if line.startswith("remote "):
                _, server, port,_ = line.split()
                if not servers == "" : servers = servers + " "
                servers = servers + server
                if not ports == "" : ports = ports + " "
                ports = ports + port
        output_line = geo + " (UDP)," + servers + "," + "udp," + ports + "\n"
        if geo[0:2] in usa: location_file_usa.write(output_line)
        if geo[0:2] in uk: location_file_uk.write(output_line)
        if geo[0:2] in eu: location_file_eu.write(output_line)
        location_file.write(output_line)
    location_file.close()
    location_file_usa.close()
    location_file_uk.close()
    location_file_eu.close()


def generatePIA():
    # Data is stored as a bunch of ovpn files
    # File name has location.  File has the server
    profiles = getProfileList("PIA")
    location_file_def = getLocations("PIA", "Default Encryption")
    location_file_strong = getLocations("PIA", "Strong Encryption")
    for profile in profiles:
        geo = profile[profile.index("PIA")+4:]
        geo = geo.replace(".ovpn", "")
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split()  
        output_line_udp_def = geo + " (UDP)," + server + "," + "udp,1198" + ",#REMOVE=1 #CERT=ca.rsa.2048.crt #CRLVERIFY=crl.rsa.2048.pem\n"
        output_line_tcp_def = geo + " (TCP)," + server + "," + "tcp,443" + ",#REMOVE=1 #CERT=ca.rsa.2048.crt #CRLVERIFY=crl.rsa.2048.pem\n"
        output_line_udp_strong = geo + " (UDP)," + server + "," + "udp,1197" + ",#REMOVE=2 #CERT=ca.rsa.4096.crt #CRLVERIFY=crl.rsa.4096.pem\n"
        output_line_tcp_strong = geo + " (TCP)," + server + "," + "tcp,443" + ",#REMOVE=2 #CERT=ca.rsa.4096.crt #CRLVERIFY=crl.rsa.4096.pem\n"
        location_file_def.write(output_line_udp_def)
        location_file_def.write(output_line_tcp_def)
        location_file_strong.write(output_line_udp_strong)
        location_file_strong.write(output_line_tcp_strong)
    location_file_def.close()
    location_file_strong.close()
        
    
def generateIPVanish():
    # Data is stored as a bunch of ovpn files
    # File name has location and most of ip address, etc
    # ipvanish-US-Seattle-sea-a04
    profiles = getProfileList("IPVanish")
    location_file = getLocations("IPVanish", "")
    for profile in profiles:
        profile = profile.replace("New-York", "New York")
        profile = profile.replace("San-Jose", "San Jose")
        profile = profile.replace("Los-Angeles", "Los Angeles")
        profile = profile.replace("LosAngeles", "Los Angeles")
        profile = profile.replace("Hong-Kong", "Hong Kong")
        profile = profile.replace("Las-Vegas", "Las Vegas")
        profile = profile.replace("Kuala-Lumpur", "Kuala Lumpur")
        profile = profile.replace("New-Delhi", "New Delhi")
        profile = profile.replace("Sao-Paulo", "Sao Paulo")
        profile = profile.replace("Buenos-Aires", "Buenos Aires")        
        tokens = profile.split("-")
        server = tokens[3] + "-" + tokens[4].replace(".ovpn", "") + ".ipvanish.com"
        server_num = tokens[4][1:3]
        output_line_udp = resolveCountry(tokens[1]) + " - " + tokens[2] + " " + server_num + " (UDP)," + server + "," + "udp,443" + "\n"
        output_line_tcp = resolveCountry(tokens[1]) + " - " + tokens[2] + " " + server_num + " (TCP)," + server + "," + "tcp,443" + "\n"
        location_file.write(output_line_udp)
        location_file.write(output_line_tcp)
    location_file.close()
    

def generateVyprVPN():
    # VyprVPN is stored in a bunch of ovpn files.  They also have an alternative set of 
    # files for Giganews customers which appear to be identical with different server names
    profiles = getProfileList("VyprVPN")
    location_file_strong = getLocations("VyprVPN", "VyprVPN Strong Encryption")
    location_file_default = getLocations("VyprVPN", "VyprVPN Default Encryption")
    location_file_giga = getLocations("VyprVPN", "Giganews Account")
    for profile in profiles:        
        geo = profile[profile.index("VyprVPN\\")+8:]
        geo = geo.replace(".ovpn", "")
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split() 
        output_line_strong = geo + " (UDP)," + server + "," + "udp," + port + "\n"
        output_line_default = geo + " (UDP)," + server + "," + "udp," + port + ",#REMOVE=1\n"
        server = server.replace("vyprvpn.com", "vpn.giganews.com")
        output_line_giga = geo + " (UDP)," + server + "," + "udp," + port + ",#REMOVE=1\n"
        location_file_strong.write(output_line_strong)
        location_file_default.write(output_line_default)
        location_file_giga.write(output_line_giga)
    location_file_strong.close()
    location_file_default.close()
    location_file_giga.close()
    
    
def generateHMA():
    # Data is stored in a flat text file
    # <Continent> - <Country>  xx.yy.rocks  random.xx.yy.rocks
    # https://www.hidemyass.com/vpn-config/ has the latest set
    location_file = getLocations("HMA", "")
    source_file = open(getUserDataPath("providers/HMA/Servers.txt"), 'r')
    source = source_file.readlines()
    source_file.close()
    for line in source:
        tokens = line.split()        
        for t in tokens:
            if ".rocks" in t and not "random." in t:
                server = t.strip(' \t\n\r')
                geo = line.replace(server, "")
                geo = geo.replace("random.", "")
                geo = geo.strip(' \t\n\r')
                geo = geo.replace("USA,", "USA -")
                geo = geo.replace("UK,", "UK -")
                output_line_udp = geo + " (UDP)," + server + "," + "udp,53" + ",#USERCERT=#PATHuser.crt #USERKEY=#PATHuser.key\n"
                output_line_tcp = geo + " (TCP)," + server + "," + "tcp,443"  + ",#USERCERT=#PATHuser.crt #USERKEY=#PATHuser.key\n"
                location_file.write(output_line_udp)
                location_file.write(output_line_tcp) 
    location_file.close()
        
    
def generatetigerVPN():
    # Data is stored in a flat text file, each line representing a connection
    # valid for UDP and TCP using the standard ports
    location_file_full = getLocations("tigerVPN", "tigerVPN Full Account")
    location_file_lite = getLocations("tigerVPN", "tigerVPN Lite Account")
    source_file = open(getUserDataPath("providers/tigerVPN/tigerVPN.csv"), 'r')
    source = source_file.readlines()
    source_file.close()
    for line in source:
        server = line.split(',')
        output_line_udp = server[1] + " " + server[0] + " (UDP)," + server[2] + "," + "udp,1194" + "\n"
        output_line_tcp = server[1] + " " + server[0] + " (TCP)," + server[2] + "," + "tcp,443"  + "\n"
        location_file_full.write(output_line_udp)
        location_file_full.write(output_line_tcp)        
        if server[4].startswith("Lite"):
            location_file_lite.write(output_line_udp)
            location_file_lite.write(output_line_tcp)
    location_file_full.close()
    location_file_lite.close()
    

def generatePureVPN():
    # Data is stored as a bunch of ovpn files
    profiles = getProfileList("PureVPN")
    location_file = getLocations("PureVPN", "")
    for profile in profiles:
        geo = profile[profile.index("PureVPN\\")+8:]
        geo = geo.replace(".ovpn", "")
        geo = geo.replace("Isle of man", "Isle Of Man")
        geo = geo.replace("MUNCHEN", "Munchen")
        geo = geo.replace("GUANGDONG", "Guangdong")
        geo = geo.replace(", ", " ")
        geo = geo.replace(",", " ")
        geo = geo.replace("1", " 1")
        geo = geo.replace("2", " 2")
        geo = geo.replace("3", " 3")
        udp_found = False
        tcp_found = False
        virtual_found = False
        if "udp" in profile: 
            udp_found = True
            proto = "udp"
            geo = geo.replace("-udp", "")            
        if "tcp" in profile: 
            tcp_found = True
            proto = "tcp"
            geo = geo.replace("-tcp", "")
        if "(V)" in profile:
            virtual_found = True
            geo = geo.replace("(V)", "")
        geo = geo.replace("-", " - ")
        if virtual_found: geo = geo + " Virtual"
        if udp_found: geo = geo + " (UDP)"
        if tcp_found: geo = geo + " (TCP)"
        profile_file = open(profile, 'r')
        lines = profile_file.readlines()
        profile_file.close()
        for line in lines:
            if line.startswith("remote "):
                _, server, port = line.split()             
        output_line = geo + "," + server + "," + proto + "," + port + "\n"
        location_file.write(output_line)
    location_file.close()


def generateNordVPN():
    # Can't use a template here as NordVPN use multiple certificate and keys. 
    # Copy the file to the target directory and rename it to something more tidy
    # Latest can be found at https://nordvpn.com/api/files/zip
    # Remove what's there to start with
    existing_profiles = glob.glob(getAddonPath(True, "NordVPN" + "/*.ovpn"))
    for connection in existing_profiles:
        xbmcvfs.delete(connection)
    # Get the list from the provider data directory
    profiles = getProfileList("NordVPN")
    destination_path = getAddonPath(True, "NordVPN" + "/")   
    for profile in profiles:
        shortname = profile[profile.index("NordVPN")+8:]
        shortname = shortname[:shortname.index(".")]
        if not "-" in shortname:
            shortname = resolveCountry((shortname[0:2]).upper()) + " " + shortname[2:]
        else:
            if "lt-lv1" in shortname: shortname = "Lithuania - Latvia 1"
            if "tw-hk1" in shortname: shortname = "Taiwan - Hong Kong 1"
            if "us-ca2" in shortname: shortname = "United States - Canada 2"
            if "nl1-ru1" in shortname: shortname = "Netherlands - Russia 1"
            if "ru-nl1" in shortname: shortname = "Russia - Netherlands 1"
            if "lv-tor1" in shortname: shortname = "Latvia TOR 1"
            if "se-tor1" in shortname: shortname = "Sweden TOR 1"
            if "nl-tor1" in shortname: shortname = "Netherlands TOR 1"
            if "nl-uk1" in shortname: shortname = "Netherlands - United Kingdom 1"
        proto = ""
        if "tcp443" in profile: proto = "(TCP)"
        if "udp1194" in profile: proto = "(UDP)"
        filename = shortname + " " + proto + ".ovpn"
        profile_file = open(profile, 'r')
        output_file = open(destination_path + filename, 'w')
        profile_contents = profile_file.readlines()
        profile_file.close()
        output = ""
        i = 0
        for line in profile_contents:
            line = line.strip(' \t\n\r')
            if not line == "" and not line.startswith("#mute") and not (i < 15 and line.startswith("#")):
                output_file.write(line + "\n")
            i = i + 1
   
   
def resolveCountry(code):   
    Countries = {'Afghanistan': 'AF',
        'Albania': 'AL',
        'Algeria': 'DZ',
        'American Samoa': 'AS',
        'Andorra': 'AD',
        'Angola': 'AO',
        'Anguilla': 'AI',
        'Antarctica': 'AQ',
        'Antigua and Barbuda': 'AG',
        'Argentina': 'AR',
        'Armenia': 'AM',
        'Aruba': 'AW',
        'Australia': 'AU',
        'Austria': 'AT',
        'Azerbaijan': 'AZ',
        'Bahamas': 'BS',
        'Bahrain': 'BH',
        'Bangladesh': 'BD',
        'Barbados': 'BB',
        'Belarus': 'BY',
        'Belgium': 'BE',
        'Belize': 'BZ',
        'Benin': 'BJ',
        'Bermuda': 'BM',
        'Bhutan': 'BT',
        'Bolivia': 'BO',
        'Bonaire, Sint Eustatius and Saba': 'BQ',
        'Bosnia and Herzegovina': 'BA',
        'Botswana': 'BW',
        'Bouvet Island': 'BV',
        'Brazil': 'BR',
        'British Indian Ocean Territory': 'IO',
        'Brunei Darussalam': 'BN',
        'Bulgaria': 'BG',
        'Burkina Faso': 'BF',
        'Burundi': 'BI',
        'Cambodia': 'KH',
        'Cameroon': 'CM',
        'Canada': 'CA',
        'Cape Verde': 'CV',
        'Cayman Islands': 'KY',
        'Central African Republic': 'CF',
        'Chad': 'TD',
        'Chile': 'CL',
        'China': 'CN',
        'Christmas Island': 'CX',
        'Cocos (Keeling) Islands': 'CC',
        'Colombia': 'CO',
        'Comoros': 'KM',
        'Congo': 'CG',
        'Congo': 'CD',
        'Cook Islands': 'CK',
        'Costa Rica': 'CR',
        'Country name': 'Code',
        'Croatia': 'HR',
        'Cuba': 'CU',
        'Curaçao': 'CW',
        'Cyprus': 'CY',
        'Czech Republic': 'CZ',
        "Côte d'Ivoire": 'CI',
        'Denmark': 'DK',
        'Djibouti': 'DJ',
        'Dominica': 'DM',
        'Dominican Republic': 'DO',
        'Ecuador': 'EC',
        'Egypt': 'EG',
        'El Salvador': 'SV',
        'Equatorial Guinea': 'GQ',
        'Eritrea': 'ER',
        'Estonia': 'EE',
        'Ethiopia': 'ET',
        'Falkland Islands (Malvinas)': 'FK',
        'Faroe Islands': 'FO',
        'Fiji': 'FJ',
        'Finland': 'FI',
        'France': 'FR',
        'French Guiana': 'GF',
        'French Polynesia': 'PF',
        'French Southern Territories': 'TF',
        'Gabon': 'GA',
        'Gambia': 'GM',
        'Georgia': 'GE',
        'Germany': 'DE',
        'Ghana': 'GH',
        'Gibraltar': 'GI',
        'Greece': 'GR',
        'Greenland': 'GL',
        'Grenada': 'GD',
        'Guadeloupe': 'GP',
        'Guam': 'GU',
        'Guatemala': 'GT',
        'Guernsey': 'GG',
        'Guinea': 'GN',
        'Guinea-Bissau': 'GW',
        'Guyana': 'GY',
        'Haiti': 'HT',
        'Heard Island and McDonald Islands': 'HM',
        'Holy See (Vatican City State)': 'VA',
        'Honduras': 'HN',
        'Hong Kong': 'HK',
        'Hungary': 'HU',
        'ISO 3166-2:GB': '(.uk)',
        'Iceland': 'IS',
        'India': 'IN',
        'Indonesia': 'ID',
        'Iran': 'IR',
        'Iraq': 'IQ',
        'Ireland': 'IE',
        'Isle of Man': 'IM',
        'Israel': 'IL',
        'Italy': 'IT',
        'Jamaica': 'JM',
        'Japan': 'JP',
        'Jersey': 'JE',
        'Jordan': 'JO',
        'Kazakhstan': 'KZ',
        'Kenya': 'KE',
        'Kiribati': 'KI',
        "North Korea": 'KP',
        'South Korea': 'KR',
        'Kuwait': 'KW',
        'Kyrgyzstan': 'KG',
        "Lao People's Democratic Republic": 'LA',
        'Latvia': 'LV',
        'Lebanon': 'LB',
        'Lesotho': 'LS',
        'Liberia': 'LR',
        'Libya': 'LY',
        'Liechtenstein': 'LI',
        'Lithuania': 'LT',
        'Luxembourg': 'LU',
        'Macao': 'MO',
        'Macedonia': 'MK',
        'Madagascar': 'MG',
        'Malawi': 'MW',
        'Malaysia': 'MY',
        'Maldives': 'MV',
        'Mali': 'ML',
        'Malta': 'MT',
        'Marshall Islands': 'MH',
        'Martinique': 'MQ',
        'Mauritania': 'MR',
        'Mauritius': 'MU',
        'Mayotte': 'YT',
        'Mexico': 'MX',
        'Micronesia': 'FM',
        'Moldova': 'MD',
        'Monaco': 'MC',
        'Mongolia': 'MN',
        'Montenegro': 'ME',
        'Montserrat': 'MS',
        'Morocco': 'MA',
        'Mozambique': 'MZ',
        'Myanmar': 'MM',
        'Namibia': 'NA',
        'Nauru': 'NR',
        'Nepal': 'NP',
        'Netherlands': 'NL',
        'New Caledonia': 'NC',
        'New Zealand': 'NZ',
        'Nicaragua': 'NI',
        'Niger': 'NE',
        'Nigeria': 'NG',
        'Niue': 'NU',
        'Norfolk Island': 'NF',
        'Northern Mariana Islands': 'MP',
        'Norway': 'NO',
        'Oman': 'OM',
        'Pakistan': 'PK',
        'Palau': 'PW',
        'Palestine': 'PS',
        'Panama': 'PA',
        'Papua New Guinea': 'PG',
        'Paraguay': 'PY',
        'Peru': 'PE',
        'Philippines': 'PH',
        'Pitcairn': 'PN',
        'Poland': 'PL',
        'Portugal': 'PT',
        'Puerto Rico': 'PR',
        'Qatar': 'QA',
        'Romania': 'RO',
        'Russia': 'RU',
        'Rwanda': 'RW',
        'Réunion': 'RE',
        'Saint Barthélemy': 'BL',
        'Saint Helena, Ascension and Tristan da Cunha': 'SH',
        'Saint Kitts and Nevis': 'KN',
        'Saint Lucia': 'LC',
        'Saint Martin (French part)': 'MF',
        'Saint Pierre and Miquelon': 'PM',
        'Saint Vincent and the Grenadines': 'VC',
        'Samoa': 'WS',
        'San Marino': 'SM',
        'Sao Tome and Principe': 'ST',
        'Saudi Arabia': 'SA',
        'Senegal': 'SN',
        'Serbia': 'RS',
        'Seychelles': 'SC',
        'Sierra Leone': 'SL',
        'Singapore': 'SG',
        'Sint Maarten (Dutch part)': 'SX',
        'Slovakia': 'SK',
        'Slovenia': 'SI',
        'Solomon Islands': 'SB',
        'Somalia': 'SO',
        'South Africa': 'ZA',
        'South Georgia and the South Sandwich Islands': 'GS',
        'South Sudan': 'SS',
        'Spain': 'ES',
        'Sri Lanka': 'LK',
        'Sudan': 'SD',
        'Suriname': 'SR',
        'Svalbard and Jan Mayen': 'SJ',
        'Swaziland': 'SZ',
        'Sweden': 'SE',
        'Switzerland': 'CH',
        'Syrian Arab Republic': 'SY',
        'Taiwan': 'TW',
        'Tajikistan': 'TJ',
        'Tanzania': 'TZ',
        'Thailand': 'TH',
        'Timor-Leste': 'TL',
        'Togo': 'TG',
        'Tokelau': 'TK',
        'Tonga': 'TO',
        'Trinidad and Tobago': 'TT',
        'Tunisia': 'TN',
        'Turkey': 'TR',
        'Turkmenistan': 'TM',
        'Turks and Caicos Islands': 'TC',
        'Tuvalu': 'TV',
        'Uganda': 'UG',
        'Ukraine': 'UA',
        'United Arab Emirates': 'AE',
        'United Kingdom': 'GB',
        'United Kingdom': 'UK',
        'United States': 'US',
        'United States Minor Outlying Islands': 'UM',
        'Uruguay': 'UY',
        'Uzbekistan': 'UZ',
        'Vanuatu': 'VU',
        'Venezuela': 'VE',
        'Vietnam': 'VN',
        'Virgin Islands, British': 'VG',
        'Virgin Islands, U.S.': 'VI',
        'Wallis and Futuna': 'WF',
        'Western Sahara': 'EH',
        'Yemen': 'YE',
        'Zambia': 'ZM',
        'Zimbabwe': 'ZW',
        'Åland Islands': 'AX',
        'Kosovo': 'XK'}   
    for c in Countries:
        if Countries[c] == code: return c        
    return code + " is unknown"
 
   