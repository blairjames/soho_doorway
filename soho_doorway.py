#!/usr/bin/env python3

import concurrent.futures
import os
from typing import Generator
import glob
import subprocess


class SohoDoorway:
    def __init__(self):
        self.log_file = os.getcwd() + "/doorway.log"

    def read_ip_file(self) -> Generator:
        try:
            pwd = os.getcwd()
            file = glob.glob(pwd + "/*.txt")
            if file:
                for f in file:
                    filer = f
                    with open(filer, "r") as file:
                        lines = (f for f in file.readlines())
                        return lines
            else:
                raise Exception
        except Exception as e:
            print("Error! in read_ip_file: " + str(e))

    def make_cmds(self, ips):
        cmds = ("/bin/whois " + i for i in ips)
        return cmds

    def substitute(self, cmds):
        with concurrent.futures.ProcessPoolExecutor(32) as pool:
            pool.map(self.who_are_you, cmds)

    def who_are_you(self, cmd):
        whois = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE)
        res = whois.stdout.decode().strip()
        with open(self.log_file, "a") as file:
            file.writelines(res)

    def clearfile(self):
        os.system("clear")
        print("Processing..\n")
        with open(self.log_file, "w") as file:
            file.write("")

    def parselog(self):
        with open(self.log_file, "r") as file:
            lines = [f for f in file.readlines()]
            for l in lines:
                if ("netname:" in l or "descr:" in l  or "org-name" in l
                    or "OrgName" in l or "NetName" in l):
                    print(l)
                    pass
                elif "NetRange:" in l or "inetnum:" in l:
                    print("\n----------------------------------\n" + l)
                    pass
            nontelstra = [l.strip() for l in lines if "etname" in l or "OrgName" in l or "org-name" in l
            and not "telstra" in l and not "TELSTRAINTERNET3-AU" in l
            and not "Telstra" in l and not "TELSTRA" in l]
            nontelstra = set(nontelstra)
            nontelstra = [n.strip() for n in nontelstra if "TELSTRA" not in n and "remarks" not in n]
            print("\nnon-Telstra entities in IP list:")
            [print(n) for n in nontelstra]

    def controller(self):
        try:
            ips = self.read_ip_file()
            ips = [i.split(" ") for i in ips if i]
            ips = [i.strip("\t").strip("\n").strip(" ").rstrip("\n") for i in ips for i in i if i]
            ips = [i for i in ips if i]
            ips = [i.split("/") for i in ips]
            ips = [i[0] for i in ips]
            cmds = self.make_cmds(ips)
            self.substitute(cmds)
            self.parselog()
            print("\nCompleted Successfully. \n\nDetails are in " + self.log_file + "\n")
        except Exception as e:
            print("Error! controller: " + str(e))

def main():
    new_soho = SohoDoorway()
    new_soho.clearfile()
    new_soho.controller()

if __name__ == '__main__':
    main()