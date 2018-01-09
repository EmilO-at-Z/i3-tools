#!/usr/bin/env python3
# vim: ts=4 sts=4 expandtab sw=4

import sys,os
import i3,json
import subprocess
import pprint

class Dmenu:
    def __init__(self, *choisesv, prompt = "select", lines = None, choises = None):
        self._prompt = prompt
        self._lines = lines
        try:
            ch = dict(choises)
            self._choises = {str(c).encode("utf-8"): ch[c] for c in ch}
        except:
            self._choises = {str(c).encode("utf-8"): c for c in (list(choises) if choises else []) + list(choisesv)}

    def __call__(self, prompt = None, lines = None):
        p = prompt if prompt else self._prompt
        l = lines if lines else self._lines
        proc = subprocess.run(
            ["dmenu", "-p", p + ":" ] + ["-l", str(l)] if l else [],
            stdout = subprocess.PIPE,
            timeout = 30,
            input = b"\n".join(self._choises.keys())
        )
        
        return self._choises[proc.stdout.strip()]



if sys.argv[1] == "layout-save":
    dest = ":".join(sorted([o["name"] for o in i3.get_outputs() if o["active"]]))

    with open(os.path.sep.join([os.environ["HOME"], ".config", "i3", "layout-" + dest]), "w") as f:
        json.dump({ws["name"] : ws["output"] for ws in i3.get_workspaces()}, indent=2, fp = f)

elif sys.argv[1] == "layout-load":
    dest = ":".join(sorted([o["name"] for o in i3.get_outputs() if o["active"]]))
    with open(os.path.sep.join([os.environ["HOME"], ".config", "i3", "layout-" + dest]), "r") as f:
        for (ws,o) in json.load(f).items():
            try:
                i3.move("workspace", "to", "output", o, workspace = ws)
            except:
                nop

elif sys.argv[1] == "workspace-to-output":
    menu = Dmenu(choises = [o["name"] for o in i3.get_outputs() if o["active"]], prompt = "outputs", lines = 5)
    i3.move("workspace", "to", "output", menu())

