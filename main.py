#!/usr/bin/env python3.7

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from pathlib import Path
from tkinter import filedialog
import tkinter.messagebox
import subprocess
import os
import re
import json
import glob

def create_file(path, empty_file):
    fo = open(path + "/" + empty_file, "w+")
    fo.close()
    return(path + "/" + empty_file)

def open_file(file_name):
    os.system("gvim "  + file_name)

def get_library_info():
    global Library_Process
    global Library_Project
    global Library_Version
    global Library_lpe_star
    global Library_Run_Dir
    global Library_CDL_TOP
    global Library_CDL_Path
    global Library_GDS_TOP
    global Library_GDS_Path
    global Library_PG_NETS
    global Library_HCELL
    global Library_SKIP_CELL
    global gProjects
    global gVersions

    lpe_config = {
                  "process":"",
                  "project":"",
                  "version":"",
                  "lpe_star":"",
                  "run_dir":os.getcwd(),
                  "cdl_top":"",
                  "cdl":"",
                  "gds_top":"",
                  "gds":"",
                  "POWER_NETS":"VSSM! VLS_4! VLS_3! VFSRDB_R! VLS_2! VSSDLL! VDLL! VFSGDL_R! VFSGT_R! VLS_1! VANTI_L! VANTI_R! VPPEX! VDDQ! VFSRDB_L! VBLPO! VBLPE! VDLY! VFSGDL_L! VFSGT_L! VP! VSSQ! VPP! VKK! VISO! VEQ! VDD! VARY! VBLP! VBB! VPLT! VSS!",
                  "hcell":"/apps/imctf/cad/script/runlpe/hcell",
                  "skip_cell":"/apps/imctf/cad/script/runlpe/skip_cell"
               }

    process = re.compile(r'^\s*process\s*=\s*(\S+)', re.I)
    project = re.compile(r'^\s*project\s*=\s*(\S+)', re.I)
    version = re.compile(r'^\s*version\s*=\s*(\S+)', re.I)
    lpe_star = re.compile(r'^\s*lpe_star\s*=\s*(\S+)', re.I)
    run_dir = re.compile(r'^\s*run_dir\s*=\s*(\S+)', re.I)
    cdl_top = re.compile(r'^\s*cdl_top\s*=\s*(\S+)', re.I)
    cdl_path = re.compile(r'^\s*cdl\s*=\s*(\S+)', re.I)
    gds_top = re.compile(r'^\s*gds_top\s*=\s*(\S+)', re.I)
    gds_path = re.compile(r'^\s*gds\s*=\s*(\S+)', re.I)
    hcell_path = re.compile(r'^\s*hcell\s*=\s*(\S+)', re.I)
    pg_nets = re.compile(r'^\s*POWER_NETS\s*=\s*(\S.*$)', re.I)

    Library_Config = Path(os.getcwd() + "/.lpe.config")
    if Library_Config.is_file() and os.path.getsize(os.getcwd() + "/.lpe.config"):
        fo = open(os.getcwd() + "/.lpe.config", "r")
        for line in fo.readlines():
            line = line.strip()
            find_process = process.match(line)
            find_project = project.match(line)
            find_version = version.match(line)
            find_lpe_star = lpe_star.match(line)
            find_run_dir = run_dir.match(line)
            find_cdl_top = cdl_top.match(line)
            find_cdl_path = cdl_path.match(line)
            find_gds_top = gds_top.match(line)
            find_gds_path = gds_path.match(line)
            find_hcell_path = hcell_path.match(line)
            find_pg_nets = pg_nets.match(line)
            
            if find_process:
                lpe_config["process"] = find_process.group(1)
            if find_project:
                lpe_config["project"] = find_project.group(1)
            if find_version:
                lpe_config["version"] = find_version.group(1)
            if find_lpe_star:
                lpe_config["lpe_star"] = find_lpe_star.group(1)
            if find_run_dir:
                lpe_config["run_dir"] = find_run_dir.group(1)
            if find_cdl_top:
                lpe_config["cdl_top"] = find_cdl_top.group(1) 
            if find_cdl_path:
                lpe_config["cdl"] = find_cdl_path.group(1)
            if find_gds_top:
                lpe_config["gds_top"] = find_gds_top.group(1)
            if find_gds_path:
                lpe_config["gds"] = find_gds_path.group(1)
            if find_hcell_path:
                lpe_config["hcell"] = find_hcell_path.group(1)
            if find_pg_nets:
                lpe_config["POWER_NETS"] = find_pg_nets.group(1)
        fo.close()
    else:
        pass
    Library_Process  = lpe_config["process"]
    Library_Project  = lpe_config["project"]

    for proc_key,proj_value in gProcessToProject.items():
        if Library_Process ==  proc_key:
            gProjects = proj_value.copy()
            
    for proj_key,ver_value in gProcjectToVersion.items():
        if Library_Project == proj_key:
            gVersions = ver_value.copy()
    
    Library_Version  = lpe_config["version"]
    Library_lpe_star  = lpe_config["lpe_star"]
    Library_Run_Dir  = lpe_config["run_dir"]
    Library_CDL_TOP  = lpe_config["cdl_top"]
    Library_CDL_Path = lpe_config["cdl"]
    Library_GDS_TOP  = lpe_config["gds_top"]
    Library_GDS_Path = lpe_config["gds"]
    Library_PG_NETS  = lpe_config["POWER_NETS"]
    Library_HCELL    = lpe_config["hcell"]
    Library_SKIP_CELL = lpe_config["skip_cell"]
    return Library_Process,Library_Project,Library_Version,Library_lpe_star,Library_Run_Dir,Library_CDL_TOP,Library_CDL_Path,Library_GDS_TOP,Library_GDS_Path,Library_PG_NETS,Library_HCELL,Library_SKIP_CELL

def write_execcmd(runDir,verify):
    exec_file = runDir + "run" + verify + ".sh"
    run = open(exec_file, "w")
    run.write('''#!/bin/bash

cd {2}

if [ {3} != "0" ];then
    echo "Please wait for {3}h before executing this task."
fi
sleep {3}h

{0}runpv -mode {1} -config {2}{1}.config |& tee {2}{1}.log
# exit
'''.format(rootpvDir,verify,runDir,WAIT_TIME.get()))
    run.close()
    subprocess.Popen("xterm -T '{0}-Flow Runing' -e 'bash -c \"source {1}; exec bash\"' &".format(verify,exec_file),shell=True)

def gen_lvs_config():
    gen_lvs_config_sub(CDL_TOP.get(),GDS_TOP.get(),"lvs")
    cellListget = load_cellList()
    if cellListget:
        for cell in cellListget:
            if cell not in [CDL_TOP.get(),GDS_TOP.get()]:
                gen_lvs_config_sub(cell,cell,"lvs")

def gen_lvs_config_sub(cdl_top,gds_top,verify):
    if cdl_top and gds_top:
        runlvs_Dir,runlvs_subRelDir = run_folder(verify,cdl_top)
        CONFIG = open(runlvs_Dir + verify + ".config", "w")
        with open(rootpvDir + verify +  ".config","r") as F_LVS:
            line = F_LVS.readline()
            while line:
                line = re.sub("^\s*process\s*=.*$","process = " + Process.get(),line)
                line = re.sub("^\s*project\s*=.*$","project = " + Project.get(),line)
                line = re.sub("^\s*version\s*=.*$","version = " + Version.get().lower(),line)
                line = re.sub("^\s*cdl\s*=.*$","cdl = " + CDL_Path.get(),line)
                line = re.sub("^\s*cdl_top\s*=.*$","cdl_top = " + cdl_top,line)
                line = re.sub("^\s*gds\s*=.*$","gds = " + GDS_Path.get(),line)
                line = re.sub("^\s*gds_top\s*=.*$","gds_top = " + gds_top,line)
                line = re.sub("^\s*hcell\s*=.*$","hcell = " + HCELL_Path.get(),line)
                line = re.sub("^\s*turbo\s*=.*$","turbo = " + Turbo_lvs.get(),line)
                line = re.sub("^\s*LVS_ABORT\s*=.*$","LVS_ABORT = " + LVS_ABORT.get(),line)
                line = re.sub("^\s*VIRTUAL_CONNECT\s*=.*$","VIRTUAL_CONNECT = " + VIRTUAL_CONNECT_LVS.get(),line)
                CONFIG.write(line)
                line = F_LVS.readline()
        CONFIG.close()
        write_execcmd(runlvs_Dir,"lvs")

def run_folder(sub_folder,gds_top):
    Run_subDir = "/".join([Run_Dir.get(),sub_folder,gds_top]) + "/"
    subprocess.call("mkdir -p " + Run_subDir,shell=True)
    Run_subRelDir = "/".join([sub_folder,gds_top])
    return Run_subDir,Run_subRelDir

def pre_check_options(sel_LayerINFO,sel_REDUCTION):
    '''
    when LayerINFO is YES, REDUCTION should not set as YES or HIGH or NO_EXTRA_LOOPS
    '''
    if sel_LayerINFO == "YES" and sel_REDUCTION in ["YES","HIGH","NO_EXTRA_LOOPS"]:
        message_info = f"confilct option: LayerINFO:{sel_LayerINFO} vs REDUCTION:{sel_REDUCTION}"
        tkinter.messagebox.showerror(title="Error",message=message_info)
        return 0
    else:
        return 1

def gen_lpe_config():
    ### pre-check for mutual exclusion options, pcao, 2023-09-04
    sel_LayerINFO = LayerINFO.get()
    sel_REDUCTION =REDUCTION.get()
    chk_flag = pre_check_options(sel_LayerINFO,sel_REDUCTION)
    if not chk_flag:
        return 0
    ### pre-check end
    gen_lpe_config_sub(CDL_TOP.get(),GDS_TOP.get(),"lpe")
    cellListget = load_cellList()
    if cellListget:
        for cell in cellListget:
            if cell not in [CDL_TOP.get(),GDS_TOP.get()]:
                gen_lpe_config_sub(cell,cell,"lpe") 

    
def gen_lpe_config_sub(cdl_top,gds_top,verify):
    if cdl_top and gds_top:
        runlpe_Dir,runlpe_subRelDir = run_folder(verify,cdl_top)
        if run_tab.select() == ".!notebook.!frame3":
            suffix_pro = "_pro"
        else:
            suffix_pro = ""
        CONFIG = open(runlpe_Dir + verify + ".config" + suffix_pro, "w+")
        with open(rootlpeDir + verify + ".config","r") as F_LPE:
            line = F_LPE.readline()
            while line:
                line = re.sub("^\s*process\s*=.*$","process = " + Process.get(),line)
                line = re.sub("^\s*project\s*=.*$","project = " + Project.get(),line)
                line = re.sub("^\s*version\s*=.*$","version = " + Version.get().lower(),line)
                line = re.sub("^\s*lpe_star\s*=.*$","lpe_star = " + lpeStar.get(),line)

                line = re.sub("^\s*pex_tf\s*=.*$","pex_tf = " + PEX_TF.get(),line)
                line = re.sub("^\s*cdl\s*=.*$","cdl = " + CDL_Path.get(),line)
                line = re.sub("^\s*cdl_top\s*=.*$","cdl_top = " + cdl_top,line)
                line = re.sub("^\s*gds\s*=.*$","gds = " + GDS_Path.get(),line)
                line = re.sub("^\s*gds_top\s*=.*$","gds_top = " + gds_top,line)
                line = re.sub("^\s*hcell\s*=.*$","hcell = " + HCELL_Path.get(),line)
                line = re.sub("^\s*skip_cell\s*=.*$","skip_cell = " + SKIP_CELL_Path.get(),line)
                line = re.sub("^\s*POWER_NETS\s*=.*$","POWER_NETS = " + POWER_NETS.get(),line)
                line = re.sub("^\s*NETS\s*=.*$","NETS = " + SELECT_NETS.get(),line)

                if run_tab.select() == ".!notebook.!frame2":
                    line = re.sub("^\s*mode\s*=.*$","mode = " + Mode.get(),line)
                    rc_mode = Mode.get()
                    line = re.sub("^\s*3D_IC\s*=.*$","3D_IC = " + threeD_IC.get(), line)
                    line = re.sub("^\s*VIRTUAL_CONNECT\s*=.*$","VIRTUAL_CONNECT = " + VIRTUAL_CONNECT.get(),line)
                    line = re.sub("^\s*CHK_LPE_LVS\s*=.*$","CHK_LPE_LVS = " + CHK_LPE_LVS.get(),line)
                    line = re.sub("^\s*POWER_EXTRACT\s*=.*$","POWER_EXTRACT = " + POWER_EXTRACT.get(),line)
                    line = re.sub("^\s*SPRES\s*=.*$","SPRES = " + SPRES.get(),line)
                    line = re.sub("^\s*NETLIST_SUBCKT\s*=.*$","NETLIST_SUBCKT = " + NETLIST_SUBCKT.get(),line)
                    line = re.sub("^\s*Core_Num\s*=.*$","Core_Num = " + CPU.get(),line) ## for calibreLPE.rule 
                    line = re.sub("^\s*R3D\s*=.*$","R3D = " + R3D.get(),line)

                if run_tab.select() == ".!notebook.!frame3":
                    line = re.sub("^\s*mode\s*=.*$","mode = " + Mode_pro.get(),line)
                    rc_mode = Mode_pro.get()
                    line = re.sub("^\s*3D_IC\s*=.*$","3D_IC = " + threeD_IC_pro.get(), line)
                    line = re.sub("^\s*VIRTUAL_CONNECT\s*=.*$","VIRTUAL_CONNECT = " + VIRTUAL_CONNECT_pro.get(),line)
                    line = re.sub("^\s*CHK_LPE_LVS\s*=.*$","CHK_LPE_LVS = " + CHK_LPE_LVS_pro.get(),line)
                    line = re.sub("^\s*POWER_EXTRACT\s*=.*$","POWER_EXTRACT = " + POWER_EXTRACT_pro.get(),line)
                    line = re.sub("^\s*Keep_Power\s*=.*$","Keep_Power = " + Keep_Power_pro.get(),line)
                    line = re.sub("^\s*SPRES\s*=.*$","SPRES = " + SPRES_pro.get(),line)
                    line = re.sub("^\s*NETLIST_SUBCKT\s*=.*$","NETLIST_SUBCKT = " + NETLIST_SUBCKT_pro.get(),line)
                    line = re.sub("^\s*Core_Num\s*=.*$","Core_Num = " + CPU_pro.get(),line) ## for calibreLPE.rule 
                    line = re.sub("^\s*R3D\s*=.*$","R3D = " + R3D_pro.get(),line)
                    line = re.sub("^\s*TOTEM\s*=.*$","TOTEM = " + TOTEM.get(),line)
                    line = re.sub("^\s*LayerINFO\s*=.*$","LayerINFO = " + LayerINFO.get(),line)
                    line = re.sub("^\s*NETLIST_INSTANCE_SECTION\s*=.*$","NETLIST_INSTANCE_SECTION = " + INSTANCE_SECTION.get(),line)
                    line = re.sub("^\s*BULK\s*=.*$","BULK = " + BULK.get(),line)
                    line = re.sub("^\s*PG_Ronly_NETS\s*=.*$","PG_Ronly_NETS = " + PG_Ronly_NETS.get(),line)
                    line = re.sub("^\s*NET_TYPE\s*=.*$","NET_TYPE = " + NET_TYPE.get(),line)
                    line = re.sub("^\s*CELL_TYPE\s*=.*$","CELL_TYPE = " + CELL_TYPE.get(),line)
                    line = re.sub("^\s*DEVICE_COORDINATE.*$","DEVICE_COORDINATE = " + DEVICE_COORDINATE.get(),line)
                    line = re.sub("^\s*REDUCTION\s*=.*$","REDUCTION = " + REDUCTION.get(),line)
                    line = re.sub("^\s*CHANGE_DEVICE_FORMAT\s*=.*$","CHANGE_DEVICE_FORMAT = " + CHANGE_DEVICE_FORMAT.get(),line)
                    line = re.sub("^\s*HIERARCHICAL_SEPARATOR\s*=.*$","HIERARCHICAL_SEPARATOR = " + HIERARCHICAL_SEPARATOR.get(),line)
                    line = re.sub("^\s*NETLIST_NODENAME_NETNAME\s*=.*$","NETLIST_NODENAME_NETNAME = " + NETLIST_NODENAME_NETNAME.get(),line)
                    line = re.sub("^\s*FLOATING_AS_FILL\s*=.*$","FLOATING_AS_FILL = " + FLOATING_AS_FILL.get(),line)
                    line = re.sub("^\s*Cap_Rep\s*=.*$","Cap_Rep = " + CAP_REP.get(),line)
                    line = re.sub("^\s*Sub_Dio\s*=.*$","Sub_Dio = " + Sub_Dio.get(),line)
                    line = re.sub("^\s*COUPLING_ABS_THRESHOLD\s*=.*$","COUPLING_ABS_THRESHOLD = " + COUPLING_ABS_THRESHOLD.get(),line)
                    line = re.sub("^\s*COUPLING_REL_THRESHOLD\s*=.*$","COUPLING_REL_THRESHOLD = " + COUPLING_REL_THRESHOLD.get(),line)
                CONFIG.write(line)
                line = F_LPE.readline()
        CONFIG.close()

        if run_tab.select() == ".!notebook.!frame3" and StarRC_Version_pro.get() == "Default":
            module = ""
            print("\nStarRC Version is Default Version!\n")
        elif run_tab.select() == ".!notebook.!frame2" and StarRC_Version.get() == "Default":
            module = ""
            print("\nStarRC Version is Default Version!\n")
        else:
            module = "module unload star/2017.12-SP3-5\nmodule load star/2020.09-SP5-4-VAL"
            print("\nStarRC Version is star/2020.09-SP5-4-VAL!\n")
        
        star_num = 1
        runlpe = open(runlpe_Dir + "runlpe.sh", "w+")
        runlpe.write('''#!/bin/bash

cd {2}
rm -rf {2}{3}{8}.log
module unload calibre/201702
module load calibre/201901_37
{4}

if [ {7} != "0" ];then
    echo "Please wait for {7}h before executing this task."
fi

sleep {7}h
bsub -Is -q star -n {5} {6}run{3} -config {2}{3}.config{8} |& tee {2}{3}{8}.log
if [ -e {0}.spf_{1} ];then
    cd ../..
    if [ -e {0}.spf_{1} ];then
        rm {0}.spf_{1}
    fi
    ln -s {3}/{0}/{0}.spf_{1} .
fi
# exit
'''.format(cdl_top, rc_mode,runlpe_Dir,verify,module,star_num,rootlpeDir,WAIT_TIME.get(),suffix_pro))
        runlpe.close()
        subprocess.Popen("xterm -T 'LPE-Flow Runing' -e 'bash -c \"source %srunlpe.sh; exec bash\"' &" % runlpe_Dir,shell=True)

def gen_drc_config():
  config = open(Run_Dir.get() + "/drc.config", "w+")
  config.write("*** CalibreDRC config file ***\n\n")
  config.write("process = " + Process.get() + "\n")
  config.write("metal = " + Metal.get() + "\n")
  config.write("gds     = " + GDS_Path.get() + "\n")
  config.write("gds_top = " + GDS_TOP.get() + "\n")
  config.close()
  rundrc()

def rundrc():
  rundrc = open("rundrc.sh", "w+")
  rundrc.write("#!/bin/bash\n\n")
  rundrc.write("cd {0}\n".format(Run_Dir.get()))
  rundrc.write("if [ ! -d 'drc' ];then\n")
  rundrc.write("mkdir drc\n")
  rundrc.write("fi\n")
  rundrc.write("cd drc\n")
  rundrc.write("rm -rf rundrc.log\n")
  rundrc.write("bsub -Is -q drc -n {0} /apps/imctf/cad/script/rundrc/rundrc -config {1}/drc.config |& tee {1}/rundrc.log\n".format(CPU.get(), Run_Dir.get()))
  rundrc.close()
  os.system("xterm -T 'DRC-Flow Runing' -e 'bash -c \"source rundrc.sh; exec bash\"'")

def runsvs(cdl1_top,cdl2_top):
    if cdl1_top and cdl2_top:
        runsvs_Dir,runsvs_subRelDir = run_folder("svs",cdl1_top)
        CONFIG = open(runsvs_Dir + "svs.config", "w")
        with open(rootpvDir + "svs.config","r") as F_SVS:
            line = F_SVS.readline()
            while line:
                line = re.sub("^\s*process\s*=.*$","process = " + Process.get(),line)
                line = re.sub("^\s*project\s*=.*$","project = " + Project.get(),line)
                line = re.sub("^\s*version\s*=.*$","version = " + Version.get().lower(),line)
                line = re.sub("^\s*cdl1\s*=.*$","cdl1 = " + CDL1_Path.get(),line)
                line = re.sub("^\s*cdl1_top\s*=.*$","cdl1_top = " + cdl1_top,line)
                line = re.sub("^\s*cdl2\s*=.*$","cdl2 = " + CDL2_Path.get(),line)
                line = re.sub("^\s*cdl2_top\s*=.*$","cdl2_top = " + cdl2_top,line)
                line = re.sub("^\s*turbo\s*=.*$","turbo = " + Turbo_svs.get(),line)
                line = re.sub("^\s*ignore_net\s*=.*$","ignore_net = " + ignore_net.get(),line)
                line = re.sub("^\s*ignore_mark\s*=.*$","ignore_mark = " + ignore_mark.get(),line)
                CONFIG.write(line)
                line = F_SVS.readline()
        CONFIG.close()
        write_execcmd(runsvs_Dir,"svs")


def runlvl(gds1_top,gds2_top):
    if gds1_top and gds2_top:
        runlvl_Dir,runlvl_subRelDir = run_folder("lvl",gds1_top)
        CONFIG = open(runlvl_Dir + "lvl.config", "w")
        with open(rootpvDir + "lvl.config","r") as F_LVL:
            line = F_LVL.readline()
            while line:
                line = re.sub("^\s*process\s*=.*$","process = " + Process.get(),line)
                line = re.sub("^\s*project\s*=.*$","project = " + Project.get(),line)
                line = re.sub("^\s*version\s*=.*$","version = " + Version.get().lower(),line)
                line = re.sub("^\s*gds1\s*=.*$","gds1 = " + GDS1_Path.get(),line)
                line = re.sub("^\s*gds1_top\s*=.*$","gds1_top = " + gds1_top,line)
                line = re.sub("^\s*gds2\s*=.*$","gds2 = " + GDS2_Path.get(),line)
                line = re.sub("^\s*gds2_top\s*=.*$","gds2_top = " + gds2_top,line)
                line = re.sub("^\s*turbo\s*=.*$","turbo = " + Turbo_lvl.get(),line)
                line = re.sub("^\s*lvl_mode\s*=.*$","lvl_mode = " + lvl_mode.get(),line)
                line = re.sub("^\s*include_layer\s*=.*$","include_layer = " + include_layer.get(),line)
                CONFIG.write(line)
                line = F_LVL.readline()
        CONFIG.close()
        write_execcmd(runlvl_Dir,"lvl")

def selectPath(Pathvar):
  Path = filedialog.askopenfilename()
  Pathvar.set(Path)

def selectCDLPath(Pathvar, entry_widget):
  Path = filedialog.askopenfilename(filetypes=[('CDL','*.cdl *.CDL *.sp *.spi'), ('All Files', '*')])
  Pathvar.set(Path)
  entry_widget.xview_moveto(1)
  
def selectGDSPath(Pathvar, entry_widget):
  Path = filedialog.askopenfilename(filetypes=[('GDS','*.gds *.GDS'), ('All Files', '*')])
  Pathvar.set(Path)
  entry_widget.xview_moveto(1)

def selectDir(Pathvar):
  Path = askdirectory()
  Pathvar.set(Path)

def lvs_result(filename):
  fo = open(filename, "r")
  if "/apps/imctf/cad/script/pvpro" in fo.read():
    message1()
  else:
    message2()
  fo.close()

def lpe_result(filename):
  fo = open(filename, "r")
  if "StarRC extraction complete" in fo.read():
    message3()
  else:
    message4()
  fo.close()

def drc_result(filename):
  fo = open(filename, "r")
  if "SUMMARY REPORT FILE = " in fo.read():
    message5()
  else:
    message6()
  fo.close()

def message1():
  tkinter.messagebox.showinfo("Great!", "Run LVS Passed!")
def message2():
  tkinter.messagebox.showerror("Sorry!", "Run LVS Failed!")
def message3():
  tkinter.messagebox.showinfo("Great!", "StarRC Extraction Compelted!")
def message4():
  tkinter.messagebox.showerror("Sorry!", "StarRC Extraction Failed!")
def message5():
  tkinter.messagebox.showinfo("Great!", "Run DRC Compelted!")
def message6():
  tkinter.messagebox.showerror("Sorry!", "Run DRC Failed!")

def usage():
  # os.popen("evince /apps/imctf/cad/script/pvpro/PVPro_GUI_Usage.pdf &")
    os.popen("evince " + gInstallDirectoryRoot + "PVPro_GUI_Usage.pdf &" )

'''
def GetPowerNets( event ):
    lvsrule = "/apps/imctf/cad/runset/" + Project.get() + "/" + Version.get().lower() + "/current/calibreLVS.rule"
    if os.path.exists( lvsrule ) and os.access( lvsrule, os.R_OK ):
        os.environ.setdefault("CALIBRE_ECHO_RULE_FILE","0")
        powerground_lines = subprocess.getoutput('/apps/mentor/calibre/cal_2017.2/bin/rules_syntax_checker {} | grep "^VARIABLE\s*\S\+_NAME"'.format(lvsrule))
        powerground_nets = re.sub(r'VARIABLE\s+\S+_NAME|"|\n',"",powerground_lines)
        powerground_names = powerground_nets.strip()

        POWER_NETS.set(powerground_names)
    else:
        POWER_NETS.set('VSSM! VLS_4! VLS_3! VFSRDB_R! VLS_2! VSSDLL! VDLL! VFSGDL_R! VFSGT_R! VLS_1! VANTI_L! VANTI_R! VPPEX! VDDQ! VFSRDB_L! VBLPO! VBLPE! VDLY! VFSGDL_L! VFSGT_L! VP! VSSQ! VPP! VKK! VISO! VEQ! VDD! VARY! VBLP! VBB! VPLT! VSS!')

'''

def GetPowerNets( event ):
    lvsrule = "/apps/imctf/cad/runset/" + Project.get() + "/" + Version.get().lower() + "/current/" + lpeStar.get() + "/calibreLPE.rule"
    if os.path.exists( lvsrule ) and os.access( lvsrule, os.R_OK ):
        includefile = subprocess.getoutput("grep 'calibreLVS_1p' {0}".format(lvsrule))
        if includefile:
            realRule = re.sub('INCLUDE\s+|"',"",includefile)
        else:
            realRule = lvsrule
        powerground_list = []
        with open(realRule,"r") as FO:
            for line in FO:
                if re.search("VARIABLE\s+POWER_NAME",line,re.I) or re.search("VARIABLE\s+GROUND_NAME",line,re.I):
                    powerground_line_prelist = re.split(r'[" \n]',line)
                    powerground_line_list = [i for i in powerground_line_prelist if i != ""]
                    powerground_line_suffix = powerground_line_list[2:]
                    powerground_list.extend(powerground_line_suffix)
            powerground_nets_list = list(set(powerground_list))
            powerground_nets_list.sort(key=powerground_list.index)
        powerground_nets = " ".join(powerground_nets_list)
        POWER_NETS.set(powerground_nets)
    else:
        POWER_NETS.set('VSSM! VLS_4! VLS_3! VFSRDB_R! VLS_2! VSSDLL! VDLL! VFSGDL_R! VFSGT_R! VLS_1! VANTI_L! VANTI_R! VPPEX! VDDQ! VFSRDB_L! VBLPO! VBLPE! VDLY! VFSGDL_L! VFSGT_L! VP! VSSQ! VPP! VKK! VISO! VEQ! VDD! VARY! VBLP! VBB! VPLT! VSS!')

def GetHcell():
    hcell_file = "/proj/" + Project.get() + "/V0/ver/lvs/hcells"
    if os.path.exists(hcell_file):
        HCELL_Path.set(hcell_file)
    else:
        HCELL_Path.set("/apps/imctf/cad/script/runlpe/hcell")


def load_cellList():
    Path = CELL_LIST.get()
    print(Path)
    if os.path.exists( Path ) and os.access( Path, os.R_OK ):
        cellList = []
        with open(Path,"r") as F_LOAD:
            for index, line in enumerate(F_LOAD):
                cellList.extend(line.split())
    else:
        cellList = []
    return cellList

def ImportJSON( path ):
    read = open( path, "r" )
    return json.load( read )

def InitialTool( path ):
    
    global rootpvDir
    global rootlpeDir
    global gProjectAndProcessInfo
    global gProjects
    global gVersions
    global gProcesses

    setting = ImportJSON( path + "initial.json" )

    rootpvDir = setting[ "rootpvDir" ]
    rootlpeDir = setting[ "rootlpeDir" ]
    gProjectAndProcessInfo = setting[ "ProjectAndProcessInfo" ]
    gProjects = setting[ "Projects" ]
    gVersions = setting[ "Versions" ]
    gProcesses = setting[ "Processes" ]

    gProjects.sort()

def InitialProjectProcessAndMetalScheme():
    global gProjects
    global gVersions
    global gProcesses
    global gProcessToProject
    global gProcjectToVersion

    read = open( gProjectAndProcessInfo, "r" )

    for line in read.readlines():
      matchObjects = re.match( r'^\s*([^#]\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', line )

      if not matchObjects is None:
        project = matchObjects.group( 1 )
        version = matchObjects.group( 2 )
        process = matchObjects.group( 3 )
        metalScheme = matchObjects.group( 4 )

        key = project.lower() + "," + version.lower() + "," + process.lower()
        
        gProcesses.append( process )
        gProjects.append( project )

        if not gProcessToProject.__contains__( process ):
            gProcessToProject[ process ] = []

        gProcessToProject[ process ].append( project )
        
        if not gProcjectToVersion.__contains__( project ):
            gProcjectToVersion[ project ] = []
        gProcjectToVersion[ project ].append( version.upper() )

    read.close()
    
    gProcesses = list( set( gProcesses ) )
    gProcesses.sort()

    gProjects = list( set( gProjects ) )
    gProjects.sort()
    

    for key in gProcessToProject.keys():
      gProcessToProject[ key ] = list( set( gProcessToProject[ key ] ) )
      gProcessToProject[ key ].sort()


def GetProjects( event ):
    Project.set( "" )
    Version.set( "" )
    lpeStar.set( "" )
    projectCombobox[ "value" ] = gProcessToProject[ Process.get() ]

def GetVersions( event ):
    Version.set( "" )
    lpeStar.set( "" )
    gVersions.clear()
    
    gVersions.extend( gProcjectToVersion[ Project.get() ] )
    versionCombobox[ "value" ] = gVersions
    
    GetHcell()

def GetLpeStar( event ):
    global gLpeStar
    lpeStar.set( "" )
    gLpeStar.clear()
    for lpePath in glob.glob( "/apps/imctf/cad/runset/" + Project.get() + "/" + Version.get().lower() + "/current/*/" ):
        lpe = lpePath.split( "/" )[ -2 ]
        matchObj = re.match( r'^lpe_star\S*', lpe )
        if matchObj:
            gLpeStar.append( lpe )
            
    lpeStarCombobox[ "value" ] = gLpeStar

def tab_change( event ):
    if run_tab.select() == ".!notebook.!frame5" or run_tab.select() == ".!notebook.!frame6":
        r4fm.grid_remove()
    else:
        nrow =  1
        r4fm.grid(row=nrow, column=0, stick=W)


def change_mode_state():
    if threeD_IC.get() == "YES":
        Mode_C.config(state=DISABLED)
        Mode_CC.config(state=DISABLED)
    else:
        Mode_C.config(state=NORMAL)
        Mode_CC.config(state=NORMAL)

def change_mode_pro_state():
    if threeD_IC_pro.get() == "YES":
        Mode_pro_C.config(state=DISABLED)
        Mode_pro_CC.config(state=DISABLED)
    else:
        Mode_pro_C.config(state=NORMAL)
        Mode_pro_CC.config(state=NORMAL)

def change_3DIC_state():
    if Mode.get() == "C" or Mode.get() == "CC":
        threeD_IC2.config(state=DISABLED) 
    else:
        threeD_IC2.config(state=NORMAL)

def change_3DIC_pro_state():
    if Mode_pro.get() == "C" or Mode_pro.get() == "CC":
        threeD_IC_pro2.config(state=DISABLED)
    else:
        threeD_IC_pro2.config(state=NORMAL)

gLpeStar = list()
gProcessToProject = dict()
gProcjectToVersion = dict()
gInstallDirectoryRoot = "/apps/imctf/cad/script/pvpro/"
InitialTool( gInstallDirectoryRoot )
InitialProjectProcessAndMetalScheme()


window = Tk()
window.title('PVPro GUI - CAD')
w_width = 900
w_height = 870
s_width = window.winfo_screenwidth()
s_height = window.winfo_screenheight()
x =  (s_width-w_width)/2
y =  (s_height-w_height)/2
window.geometry("+%d+%d" % (x,y))

Library_Process, Library_Project, Library_Version, Library_lpe_star, Library_Run_Dir, Library_CDL_TOP, Library_CDL_Path, Library_GDS_TOP, Library_GDS_Path, Library_PG_NETS, Library_HCELL, Library_SKIP_CELL = get_library_info()

# Project frame set
comboboxWidth = 14
nrow = 0
r1fm = LabelFrame(window,text="Project Set",font=("Times New Roman", "16",'bold'))

processLabel = Label(r1fm, text=' Process', height=1, anchor='w',font=("Fixdsys",'13')).grid(row=0, column=0,ipadx = 5, ipady = 5,  stick=W)
Process = StringVar()
Process.set(Library_Process)
processCombobox = ttk.Combobox( r1fm, textvariable = Process, width = 14 )
processCombobox[ "value" ] = gProcesses
processCombobox.bind( "<<ComboboxSelected>>", GetProjects )
processCombobox.grid( row = 0, column = 1,ipadx = 5, ipady = 5, sticky = W )

projectLabel = Label( r1fm, text = "Project", anchor = "w" , font=("Fixdsys",'13') )
projectLabel.grid( row = 0, column = 2, ipadx = 5, ipady = 5, sticky = "w" )
Project = StringVar()
Project.set(Library_Project)
projectCombobox = ttk.Combobox( r1fm, textvariable = Project, width = 14 )
projectCombobox[ "value" ] = gProjects
projectCombobox.bind( "<<ComboboxSelected>>", GetVersions )
projectCombobox.grid( row = 0, column = 3,ipadx = 5, ipady = 5, sticky = "w" )

versionLabel = Label( r1fm, text = "Version", anchor = "w" , font=("Fixdsys",'13') )
versionLabel.grid( row = 0, column = 4, ipadx = 5, ipady = 5,sticky = "w" )
Version = StringVar()
Version.set(Library_Version)
versionCombobox = ttk.Combobox( r1fm, textvariable = Version, width = 14 )
versionCombobox[ "value" ] = gVersions
versionCombobox.bind( "<<ComboboxSelected>>", GetLpeStar )
versionCombobox.grid( row = 0, column = 5,ipadx = 5, ipady = 5, sticky = "w" )

lpeStarLabel = Label( r1fm, text = "lpe_star", anchor = "w" , font=("Fixdsys",'13') )
lpeStarLabel.grid( row = 1, column = 0, ipadx = 5, ipady = 5,sticky = "w" )
lpeStar = StringVar()
lpeStar.set(Library_lpe_star)
lpeStarCombobox = ttk.Combobox( r1fm, textvariable = lpeStar, width = 14 )
lpeStarCombobox[ "value" ] = gLpeStar
lpeStarCombobox.bind( "<<ComboboxSelected>>", GetPowerNets )
lpeStarCombobox.grid( row = 1, column = 1,ipadx = 5, ipady = 5, sticky = "w" )
r1fm.grid(row=nrow, column=0, stick=W)

# Logo frame set 
r2fm = Frame(window)
logo_path = "/apps/imctf/cad/script/pvpro/logo.gif"
logo_file = PhotoImage(file=logo_path)
Label(r2fm, text='* Click Logo: Usage *',height=1).grid(row=0, column=0, stick=E)
Button(r2fm, image = logo_file, command=usage).grid(row=1, column=0, stick=E)
Label(r2fm, text=' Owner: Kobe Weng', height=1).grid(row=2, column=0, stick=E)
Label(r2fm, text='', height=1).grid(row=3, column=0, stick=E)
r2fm.grid(row=nrow, column=1, stick=E)

# Run frame set 
nrow = nrow + 1
r3fm = Frame(window,height=100, width=100)
Button(r3fm, text=' Run-LVS', command=gen_lvs_config, width=5, height=1, bd=5, activebackground='green', bg='gold').grid(row=4, column=0, ipadx=5, ipady=5, stick=E)
Label(r3fm, text='', height=1).grid(row=5, column=0, stick=E)
Button(r3fm, text=' Run-LPE', command=gen_lpe_config, width=5, height=1, bd=5, activebackground='green', bg='gold').grid(row=6, column=0, ipadx=5, ipady=5, stick=E)
Label(r3fm, text='', height=1).grid(row=7, column=0, stick=E)
Button(r3fm, text=' Run-DRC', command=gen_drc_config, width=5, height=1, bd=5, activebackground='green', bg='gold').grid(row=8, column=0, ipadx=5, ipady=5, stick=E)
Label(r3fm, text='', height=1).grid(row=9, column=0, stick=E)
Button(r3fm, text=' Run-SVS', command=lambda: runsvs(CDL1_TOP.get(),CDL2_TOP.get()), width=5, height=1, bd=5, activebackground='green', bg='gold').grid(row=10, column=0, ipadx=5, ipady=5, stick=E)
Label(r3fm, text='', height=1).grid(row=11, column=0, stick=E)
Button(r3fm, text=' Run-LVL', command=lambda: runlvl(GDS1_TOP.get(),GDS2_TOP.get()), width=5, height=1, bd=5, activebackground='green', bg='gold').grid(row=12, column=0, ipadx=5, ipady=5, stick=E)
Label(r3fm, text='', height=1).grid(row=13, column=0, stick=E)
Button(r3fm, text=' Exit', command=window.quit, width=5, height=1, bd=5, activebackground='red', bg='gold').grid(row=14, column=0, ipadx=5, ipady=5, stick=E)
r3fm.grid(row=nrow, column=1, stick=E)

# Run file set 
r4fm = LabelFrame(window,text="File Set",font=("Times New Roman", "16",'bold'))
PEX_TF = StringVar()
Run_Dir = StringVar()
CDL_TOP = StringVar()
CDL_Path = StringVar()
GDS_TOP = StringVar()
GDS_Path = StringVar()
HCELL_Path = StringVar()
SKIP_CELL_Path = StringVar()
POWER_NETS = StringVar()
PEX_TF.set('current')
Run_Dir.set(Library_Run_Dir)
SELECT_NETS = StringVar()
CDL_TOP.set(Library_CDL_TOP)
CDL_Path.set(Library_CDL_Path)
GDS_TOP.set(Library_GDS_TOP)
GDS_Path.set(Library_GDS_Path)
HCELL_Path.set(Library_HCELL)
SKIP_CELL_Path.set(Library_SKIP_CELL)
# POWER_NETS.set('VSSM! VLS_4! VLS_3! VFSRDB_R! VLS_2! VSSDLL! VDLL! VFSGDL_R! VFSGT_R! VLS_1! VANTI_L! VANTI_R! VPPEX! VDDQ! VFSRDB_L! VBLPO! VBLPE! VDLY! VFSGDL_L! VFSGT_L! VP! VSSQ! VPP! VKK! VISO! VEQ! VDD! VARY! VBLP! VBB! VPLT! VSS!')
POWER_NETS.set(Library_PG_NETS)
SELECT_NETS.set('*')
PEX_TF1 = Label(r4fm, text=" PEX_TF", anchor='w', width=7, height=1).grid(row=0, column=0, ipadx=5, ipady=5, stick=W)
PEX_TF2 = Entry(r4fm, width=10, textvariable=PEX_TF).grid(row=0, column=1, ipadx=5, ipady=5, stick=W)
Run_Dir1 = Label(r4fm, text=" Run_Dir", anchor='w', width=7, height=1).grid(row=1, column=0, ipadx=5, ipady=5, stick=W)
Run_Dir2 = Entry(r4fm, width=50, textvariable=Run_Dir).grid(row=1, column=1, ipadx=5, ipady=5, stick=W)
Run_Dir3 = Button(r4fm, text="Select", command=lambda Pathvar=Run_Dir: selectDir(Pathvar)).grid(row=1, column=2)
CDL1 = Label(r4fm, text=' CDL_TOP', anchor='w', width=7, height=1).grid(row=2, column=0, ipadx=5, ipady=5, stick=W)
CDL2 = Entry(r4fm, width=50, textvariable=CDL_TOP).grid(row=2, column=1, ipadx=5, ipady=5, stick=W)
CDL3 = Label(r4fm, text=" CDL_Path", anchor='w', width=7, height=1).grid(row=3, column=0, ipadx=5, ipady=5, stick=W)
CDL4 = Entry(r4fm, width=50, textvariable=CDL_Path)
CDL4.grid(row=3, column=1, ipadx=5, ipady=5, stick=W)
CDL5 = Button(r4fm, text="Select", command=lambda Pathvar=CDL_Path, entry_widget=CDL4: selectCDLPath(Pathvar, entry_widget)).grid(row=3, column=2)
GDS1 = Label(r4fm, text=' GDS_TOP', anchor='w', width=7, height=1).grid(row=4, column=0, ipadx=5, ipady=5, stick=W)
GDS2 = Entry(r4fm, width=50, textvariable=GDS_TOP).grid(row=4, column=1, ipadx=5, ipady=5, stick=W)
GDS3 = Label(r4fm, text=" GDS_Path", anchor='w', width=7, height=1).grid(row=5, column=0, ipadx=5, ipady=5, stick=W)
GDS4 = Entry(r4fm, width=50, textvariable=GDS_Path)
GDS4.grid(row=5, column=1, ipadx=5, ipady=5, stick=W)
GDS5 = Button(r4fm, text="Select", command=lambda Pathvar=GDS_Path, entry_widget=GDS4: selectGDSPath(Pathvar, entry_widget)).grid(row=5, column=2)
HCELL1 = Label(r4fm, text=" Hcell", anchor='w', width=7, height=1).grid(row=6, column=0, ipadx=5, ipady=5, stick=W)
HCELL2 = Entry(r4fm, width=50, textvariable=HCELL_Path).grid(row=6, column=1, ipadx=5, ipady=5, stick=W)
HCELL3 = Button(r4fm, text="Select", command=lambda Pathvar=HCELL_Path: selectPath(Pathvar)).grid(row=6, column=2)
HCELL4 = Button(r4fm, text="Open", command=lambda:open_file(HCELL_Path.get())).grid(row=6, column=3)
SKIP_CELL1 = Label(r4fm, text=" SKIP_CELL", anchor='w', width=7, height=1).grid(row=7, column=0, ipadx=5, ipady=5, stick=W)
SKIP_CELL2 = Entry(r4fm, width=50, textvariable=SKIP_CELL_Path).grid(row=7, column=1, ipadx=5, ipady=5, stick=W)
SKIP_CELL3 = Button(r4fm, text="Select", command=lambda Pathvar=SKIP_CELL_Path: selectPath(Pathvar)).grid(row=7, column=2)
SKIP_CELL4 = Button(r4fm, text="Open", command=lambda:open_file(SKIP_CELL_Path.get())).grid(row=7, column=3)
POWER1 = Label(r4fm, text=" POWER_NETS", anchor='w', width=15, height=1).grid(row=8, column=0, ipadx=5, ipady=5, stick=W)
POWER2 = Entry(r4fm, width=50, textvariable=POWER_NETS).grid(row=8, column=1, ipadx=5, ipady=5, stick=W)
SELECT_NETS1 = Label(r4fm, text=' SELECT_NETS', width=15, height=1, anchor='w').grid(row=9, column=0, ipadx=5, ipady=5, stick=W)
SELECT_NETS1 = Entry(r4fm, width=50, textvariable=SELECT_NETS).grid(row=9, column=1, ipadx=5, ipady=5, stick=W)
CELL_LIST = StringVar()
CELL_LIST.set("")
cellListLabel = Label(r4fm, text=" CELL_LIST", width=15, height=1 ,anchor='w').grid(row=10, column=0, ipadx=5, ipady=5, stick=W)
cellListEntry = Entry(r4fm, width=50, textvariable=CELL_LIST).grid(row=10, column=1, ipadx=5, ipady=5, stick=W)
cellListButton1 = Button(r4fm, text="Select", command=lambda Pathvar=CELL_LIST: selectPath(Pathvar)).grid(row=10, column=2)
cellListButton2 = Button(r4fm, text="Open", command=lambda:open_file(CELL_LIST.get())).grid(row=10, column=3)
WAIT_TIME = StringVar()
WAIT_TIME.set("0")
waitTimeLabel = Label(r4fm, text=" WAIT_TIME", width=15, height=1 ,anchor='w').grid(row=11, column=0, ipadx=5, ipady=5, stick=W)
waitTimeEntry = Entry(r4fm, width=50, textvariable=WAIT_TIME).grid(row=11, column=1, ipadx=5, ipady=5, stick=W)
clock_file = PhotoImage(file=gInstallDirectoryRoot+ "clock.PNG")
Label(r4fm, image=clock_file).grid(row=11, column=2)
r4fm.grid(row=nrow, column=0, stick=W)

# Validation settings
nrow = nrow + 1
basic_row = 0
ttk_style = ttk.Style()
Mysky = "#DCF0F2"
Myyellow = "#F2C84B"
ttk_style.theme_create( "dummy", parent="alt", settings={
          "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
          "TNotebook.Tab": {
                          "configure": {"padding": [5, 1], "background": Mysky, "font": ("Times New Roman", "15",'bold')},
                          "map":       {"background": [("selected", Myyellow)],
                          "expand": [("selected", [1, 1, 1, 0])] }
                           }
                                                        } 
                      )
ttk_style.theme_use("dummy")
run_tab = ttk.Notebook(window)
run_tab.bind('<<NotebookTabChanged>>', tab_change)

# lvs setting
lvs_frame = Frame(run_tab)
lvs_tab = run_tab.add(lvs_frame,text = "LVS ")

Label(lvs_frame, text='  Turbo', height=1, anchor='w').grid(row=0, column=0, ipadx=5, ipady=5, stick=W)
Turbo_lvs = StringVar()
Turbo_lvs.set('4')
Turbo_lvs1= Radiobutton(lvs_frame, text=' 1', width=7, anchor='w', variable=Turbo_lvs, value='1').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
Turbo_lvs2= Radiobutton(lvs_frame, text=' 4', width=7, anchor='w', variable=Turbo_lvs, value='4').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
Turbo_lvs3= Radiobutton(lvs_frame, text=' 8', width=7, anchor='w', variable=Turbo_lvs, value='8').grid(row=basic_row, column=3, ipadx=5, ipady=5, stick=W)
Turbo_lvs4 = Radiobutton(lvs_frame, text=' 16', width=7, anchor='w', variable=Turbo_lvs, value='16').grid(row=basic_row, column=4, ipadx=5, ipady=5, stick=W)
Turbo_lvs5 = Radiobutton(lvs_frame, text=' 32', width=7, anchor='w', variable=Turbo_lvs, value='32').grid(row=basic_row, column=5, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
Label(lvs_frame, text=' VIRTUAL_CONNET', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
VIRTUAL_CONNECT_LVS = StringVar()
VIRTUAL_CONNECT_LVS.set('NO')
VIRTUAL_CONNECT_LVS1 = Radiobutton(lvs_frame, text=' NO', width=7, anchor='w', variable=VIRTUAL_CONNECT_LVS, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
VIRTUAL_CONNECT_LVS2 = Radiobutton(lvs_frame, text=' YES', width=7, anchor='w', variable=VIRTUAL_CONNECT_LVS, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
LVS_ABORT = StringVar()
LVS_ABORT.set('YES')
Label(lvs_frame, text=' LVS_ABORT', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
LVS_ABORT1 = Radiobutton(lvs_frame, text=' NO', width=7, anchor='w', variable=LVS_ABORT, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
LVS_ABORT2 = Radiobutton(lvs_frame, text=' YES', width=7, anchor='w', variable=LVS_ABORT, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

# lpe normal setting
lpe_frame_normal = Frame(run_tab)
lpe_tab = run_tab.add(lpe_frame_normal,text = "LPE ")

basic_row = 0
Mode = StringVar()
Mode.set('RC')
Label(lpe_frame_normal, text=' RC Mode', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
Mode_R = Radiobutton(lpe_frame_normal, text=' R-only', width=7, anchor='w', variable=Mode, value='R', command=change_3DIC_state)
Mode_R.grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
Mode_C = Radiobutton(lpe_frame_normal, text=' C-only', width=7, anchor='w', variable=Mode, value='C', command=change_3DIC_state) 
Mode_C.grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
Mode_RC = Radiobutton(lpe_frame_normal, text=' RC', width=7, anchor='w', variable=Mode, value='RC', command=change_3DIC_state)
Mode_RC.grid(row=basic_row, column=3, ipadx=5, ipady=5, stick=W)
Mode_CC = Radiobutton(lpe_frame_normal, text=' CC', width=7, anchor='w', variable=Mode, value='CC', command=change_3DIC_state)
Mode_CC.grid(row=basic_row, column=4, ipadx=5, ipady=5, stick=W)
Mode_RCC = Radiobutton(lpe_frame_normal, text=' RCC', width=7, anchor='w', variable=Mode, value='RCC', command=change_3DIC_state)
Mode_RCC.grid(row=basic_row, column=5, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
Label(lpe_frame_normal, text=' 3D_IC', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5,ipady=5, stick=W)
threeD_IC = StringVar()
threeD_IC.set('NO')
threeD_IC1 = Radiobutton(lpe_frame_normal, text=' NO', width=7, anchor='w', variable=threeD_IC, value='NO',command=change_mode_state)
threeD_IC1.grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
threeD_IC2 = Radiobutton(lpe_frame_normal, text=' YES', width=7, anchor='w', variable=threeD_IC, value='YES',command=change_mode_state)
threeD_IC2.grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
Label(lpe_frame_normal, text=' VIRTUAL_CONNET', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
VIRTUAL_CONNECT = StringVar()
VIRTUAL_CONNECT.set('NO')
VIRTUAL_CONNECT1 = Radiobutton(lpe_frame_normal, text=' NO', width=7, anchor='w', variable=VIRTUAL_CONNECT, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
VIRTUAL_CONNECT2 = Radiobutton(lpe_frame_normal, text=' YES', width=7, anchor='w', variable=VIRTUAL_CONNECT, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
CHK_LPE_LVS = StringVar()
CHK_LPE_LVS.set('YES')
Label(lpe_frame_normal, text=' CHK_LPE_LVS', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
CHK_LPE_LVS1 = Radiobutton(lpe_frame_normal, text=' NO', width=7, anchor='w', variable=CHK_LPE_LVS, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
CHK_LPE_LVS2 = Radiobutton(lpe_frame_normal, text=' YES', width=7, anchor='w', variable=CHK_LPE_LVS, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
POWER_EXTRACT = StringVar()
POWER_EXTRACT.set('LRSD')
Label(lpe_frame_normal, text=' POWER_EXTRACT', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
POWER_EXTRACT1 = Radiobutton(lpe_frame_normal, text=' NO', width=7, anchor='w', variable=POWER_EXTRACT, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
POWER_EXTRACT2 = Radiobutton(lpe_frame_normal, text=' YES', width=7, anchor='w', variable=POWER_EXTRACT, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
POWER_EXTRACT3 = Radiobutton(lpe_frame_normal, text=' LRSD', width=7, anchor='w', variable=POWER_EXTRACT, value='LRSD').grid(row=basic_row, column=3, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
SPRES = StringVar()
SPRES.set('NO')
Label(lpe_frame_normal, text=' SPRES', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
SPRES1 = Radiobutton(lpe_frame_normal, text=' NO', width=7, anchor='w', variable=SPRES, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
SPRES2 = Radiobutton(lpe_frame_normal, text=' YES', width=7, anchor='w', variable=SPRES, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
NETLIST_SUBCKT = StringVar()
NETLIST_SUBCKT.set('YES')
Label(lpe_frame_normal, text=' NETLIST_SUBCKT', bg='green', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
NETLIST_SUBCKT1 = Radiobutton(lpe_frame_normal, text=' NO', width=7, anchor='w', variable=NETLIST_SUBCKT, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
NETLIST_SUBCKT2 = Radiobutton(lpe_frame_normal, text=' YES', width=7, anchor='w', variable=NETLIST_SUBCKT, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
CPU = StringVar()
CPU.set('1')
Label(lpe_frame_normal, text='CPU_Core_Num', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
CPU1 = Radiobutton(lpe_frame_normal, text=' 1', width=7, anchor='w', variable=CPU, value='1').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
CPU2 = Radiobutton(lpe_frame_normal, text=' 4', width=7, anchor='w', variable=CPU, value='4').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
CPU3 = Radiobutton(lpe_frame_normal, text=' 8', width=7, anchor='w', variable=CPU, value='8').grid(row=basic_row, column=3, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
R3D = StringVar()
R3D.set('NO')
R3D_Label = Label(lpe_frame_normal, text=' R3D', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
R3D1 = Radiobutton(lpe_frame_normal, text=' NO', width=7, anchor='w', variable=R3D, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
R3D2 = Radiobutton(lpe_frame_normal, text=' YES', width=7, anchor='w', variable=R3D, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
StarRC_Version = StringVar()
StarRC_Version.set('2020')
Label(lpe_frame_normal, text=' StarRC_Version', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
StarRC1 = Radiobutton(lpe_frame_normal, text=' Default', width=7, anchor='w', variable=StarRC_Version, value='Default').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
StarRC2 = Radiobutton(lpe_frame_normal, text=' 2020', width=7, anchor='w', variable=StarRC_Version, value='2020').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

# lpe professional setting
lpe_frame_adv = Frame(run_tab)
lpe_tab = run_tab.add(lpe_frame_adv,text = "LPE_pro ")
canvas = Canvas(lpe_frame_adv, width=660,height=300)
vsb = ttk.Scrollbar(lpe_frame_adv, orient="vertical", cursor='hand2', command=canvas.yview)
canvas.grid(row=1, column=0, sticky="news")
canvas.config(yscrollcommand=vsb.set)
vsb.grid(row=1, column=1, sticky='ns')
lpe_frame = Frame(canvas)
canvas.create_window(0, 0, window=lpe_frame, anchor = 'nw')

basic_row = 0
Label(lpe_frame, text=' RC Mode', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
Mode_pro = StringVar()
Mode_pro.set('RC')
Mode_pro_R = Radiobutton(lpe_frame, text=' R-only', width=7, anchor='w', variable=Mode_pro, value='R', command=change_3DIC_pro_state)
Mode_pro_R.grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
Mode_pro_C = Radiobutton(lpe_frame, text=' C-only', width=7, anchor='w', variable=Mode_pro, value='C', command=change_3DIC_pro_state)
Mode_pro_C.grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
Mode_pro_RC = Radiobutton(lpe_frame, text=' RC', width=7, anchor='w', variable=Mode_pro, value='RC', command=change_3DIC_pro_state)
Mode_pro_RC.grid(row=basic_row, column=3, ipadx=5, ipady=5, stick=W)
Mode_pro_CC = Radiobutton(lpe_frame, text=' CC', width=7, anchor='w', variable=Mode_pro, value='CC', command=change_3DIC_pro_state)
Mode_pro_CC.grid(row=basic_row, column=4, ipadx=5, ipady=5, stick=W)
Mode_pro_RCC = Radiobutton(lpe_frame, text=' RCC', width=7, anchor='w', variable=Mode_pro, value='RCC', command=change_3DIC_pro_state)
Mode_pro_RCC.grid(row=basic_row, column=5, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
Label(lpe_frame, text=' 3D_IC', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5,ipady=5, stick=W)
threeD_IC_pro = StringVar()
threeD_IC_pro.set('NO')
threeD_IC_pro1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=threeD_IC_pro, value='NO', command=change_mode_pro_state)
threeD_IC_pro1.grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
threeD_IC_pro2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=threeD_IC_pro, value='YES', command=change_mode_pro_state)
threeD_IC_pro2.grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
Label(lpe_frame, text=' VIRTUAL_CONNET', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
VIRTUAL_CONNECT_pro = StringVar()
VIRTUAL_CONNECT_pro.set('YES')
VIRTUAL_CONNECT_pro1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=VIRTUAL_CONNECT_pro, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
VIRTUAL_CONNECT_pro2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=VIRTUAL_CONNECT_pro, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
CHK_LPE_LVS_pro = StringVar()
CHK_LPE_LVS_pro.set('YES')
Label(lpe_frame, text=' CHK_LPE_LVS', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
CHK_LPE_LVS_pro1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=CHK_LPE_LVS_pro, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
CHK_LPE_LVS_pro2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=CHK_LPE_LVS_pro, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
POWER_EXTRACT_pro = StringVar()
POWER_EXTRACT_pro.set('LRSD')
Label(lpe_frame, text=' POWER_EXTRACT', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
POWER_EXTRACT_pro1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=POWER_EXTRACT_pro, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
POWER_EXTRACT_pro2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=POWER_EXTRACT_pro, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
POWER_EXTRACT_pro3 = Radiobutton(lpe_frame, text=' LRSD', width=7, anchor='w', variable=POWER_EXTRACT_pro, value='LRSD').grid(row=basic_row, column=3, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
Keep_Power_pro = StringVar()
Keep_Power_pro.set('ALL')
Keep_Power_Lable = Label(lpe_frame, text=" Keep_Power", anchor='w', width=15, height=1).grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
Keep_Power_Entry = Entry(lpe_frame, width=24, textvariable=Keep_Power_pro).grid(row=basic_row, column=1, ipadx=5, ipady=5, columnspan=2, stick=W)

basic_row = basic_row + 1
SPRES_pro = StringVar()
SPRES_pro.set('NO')
Label(lpe_frame, text=' SPRES', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
SPRES_pro1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=SPRES_pro, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
SPRES_pro2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=SPRES_pro, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
NETLIST_SUBCKT_pro = StringVar()
NETLIST_SUBCKT_pro.set('YES')
Label(lpe_frame, text=' NETLIST_SUBCKT', bg='green', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
NETLIST_SUBCKT_pro1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=NETLIST_SUBCKT_pro, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
NETLIST_SUBCKT_pro2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=NETLIST_SUBCKT_pro, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
CPU_pro = StringVar()
CPU_pro.set('1')
Label(lpe_frame, text='CPU_Core_Num', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
CPU_pro1 = Radiobutton(lpe_frame, text=' 1', width=7, anchor='w', variable=CPU_pro, value='1').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
CPU_pro2 = Radiobutton(lpe_frame, text=' 4', width=7, anchor='w', variable=CPU_pro, value='4').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
CPU_pro3 = Radiobutton(lpe_frame, text=' 8', width=7, anchor='w', variable=CPU_pro, value='8').grid(row=basic_row, column=3, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
LayerINFO = StringVar()
LayerINFO.set('NO')
Label(lpe_frame, text='Layer Info', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
LayerINFO1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=LayerINFO, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
LayerINFO2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=LayerINFO, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
R3D_pro = StringVar()
R3D_pro.set('NO')
R3D_pro_Label = Label(lpe_frame, text=' R3D', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
R3D_pro1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=R3D_pro, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
R3D_pro2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=R3D_pro, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
TOTEM = StringVar()
TOTEM.set('NO')
Label(lpe_frame, text=' TOTEM', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
TOTEM1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=TOTEM, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
TOTEM2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=TOTEM, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
StarRC_Version_pro = StringVar()
StarRC_Version_pro.set('2020')
Label(lpe_frame, text=' StarRC_Version', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
StarRC1 = Radiobutton(lpe_frame, text=' Default', width=7, anchor='w', variable=StarRC_Version_pro, value='Default').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
StarRC2 = Radiobutton(lpe_frame, text=' 2020', width=7, anchor='w', variable=StarRC_Version_pro, value='2020').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
CHANGE_DEVICE_FORMAT = StringVar()
CHANGE_DEVICE_FORMAT.set('YES')
CHANGE_DEVICE_FORMAT_Label = Label(lpe_frame, text=' CHANGE_DEV', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
CHANGE_DEVICE_FORMAT1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=CHANGE_DEVICE_FORMAT, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
CHANGE_DEVICE_FORMAT2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=CHANGE_DEVICE_FORMAT, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
INSTANCE_SECTION = StringVar()
INSTANCE_SECTION.set('SELECTED') 
INSTANCE_SECTION_Label = Label(lpe_frame, text=' INSTANCE_SECTION', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
INSTANCE_SECTION1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=INSTANCE_SECTION, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
INSTANCE_SECTION3 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=INSTANCE_SECTION, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
INSTANCE_SECTION2 = Radiobutton(lpe_frame, text=' SELECTED', width=7, anchor='w', variable=INSTANCE_SECTION, value='SELECTED').grid(row=basic_row, column=3, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
BULK = StringVar()
BULK.set('NO')
BULK_Label = Label(lpe_frame, text=' BULK', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
BULK1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=BULK, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
BULK2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=BULK, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
BULK3 = Radiobutton(lpe_frame, text=' CONLY', width=7, anchor='w', variable=BULK, value='CONLY').grid(row=basic_row, column=3, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
PG_Ronly_NETS = StringVar()
PG_Ronly_NETS.set('')
PR_NETS1_Lable = Label(lpe_frame, text=" PG_Ronly_NETS", anchor='w', width=15, height=1).grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
PR_NETS2_Entry = Entry(lpe_frame, width=24, textvariable=PG_Ronly_NETS).grid(row=basic_row, column=1, ipadx=5, ipady=5, columnspan=2, stick=W)

basic_row = basic_row + 1
NET_TYPE = StringVar()
NET_TYPE.set('LAYOUT')
NET_TYPE_Label = Label(lpe_frame, text=' NET_TYPE', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
NET_TYPE1 = Radiobutton(lpe_frame, text=' SCH', width=7, anchor='w', variable=NET_TYPE, value='SCHEMATIC').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
NET_TYPE2 = Radiobutton(lpe_frame, text=' LAYOUT', width=7, anchor='w', variable=NET_TYPE, value='LAYOUT').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
CELL_TYPE = StringVar()
CELL_TYPE.set('LAYOUT')
CELL_TYPE_Label = Label(lpe_frame, text=' CELL_TYPE', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
CELL_TYPE1 = Radiobutton(lpe_frame, text=' SCH', width=7, anchor='w', variable=CELL_TYPE, value='SCHEMATIC').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
CELL_TYPE2 = Radiobutton(lpe_frame, text=' LAYOUT', width=7, anchor='w', variable=CELL_TYPE, value='LAYOUT').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
DEVICE_COORDINATE = StringVar()
DEVICE_COORDINATE.set('NO')
DEVICE_COORDINATE_Label = Label(lpe_frame, text=' DEV_COORDINATE', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
DEVICE_COORDINATE1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=DEVICE_COORDINATE, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
DEVICE_COORDINATE2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=DEVICE_COORDINATE, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
DEVICE_COORDINATE3 = Radiobutton(lpe_frame, text=' COMMENT', width=7, anchor='w', variable=DEVICE_COORDINATE, value='COMMENT').grid(row=basic_row, column=3, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
REDUCTION = StringVar()
REDUCTION.set('NO')
REDUCTION_Label = Label(lpe_frame, text=' REDUCTION', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
REDUCTION1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=REDUCTION, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
REDUCTION2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=REDUCTION, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
REDUCTION3 = Radiobutton(lpe_frame, text=' HIGH', width=7, anchor='w', variable=REDUCTION, value='HIGH').grid(row=basic_row, column=3, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
HIERARCHICAL_SEPARATOR = StringVar()
HIERARCHICAL_SEPARATOR.set('.')
HIERARCHICAL_SEPARATOR_Label = Label(lpe_frame, text=' HIERARCHICAL', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
HIERARCHICAL_SEPARATOR1 = Radiobutton(lpe_frame, text=' /', width=7, anchor='w', variable=HIERARCHICAL_SEPARATOR, value='/').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
HIERARCHICAL_SEPARATOR2 = Radiobutton(lpe_frame, text=' .', width=7, anchor='w', variable=HIERARCHICAL_SEPARATOR, value='.').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
NETLIST_NODENAME_NETNAME = StringVar()
NETLIST_NODENAME_NETNAME.set('YES')
NETLIST_NODENAME_NETNAME_Label = Label(lpe_frame, text=' RETAIN_NET', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
NETLIST_NODENAME_NETNAME1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=NETLIST_NODENAME_NETNAME, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
NETLIST_NODENAME_NETNAME2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=NETLIST_NODENAME_NETNAME, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
FLOATING_AS_FILL = StringVar()
FLOATING_AS_FILL.set('NO')
FLOATING_AS_FILL_Label = Label(lpe_frame, text=' FLOATING_AS_FILL', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
FLOATING_AS_FILL1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=FLOATING_AS_FILL, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
FLOATING_AS_FILL2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=FLOATING_AS_FILL, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
CAP_REP = StringVar()
CAP_REP.set('NO')
CAP_REP_Label = Label(lpe_frame, text=' CAP_REP', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
CAP_REP1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=CAP_REP, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
CAP_REP2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=CAP_REP, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
Sub_Dio = StringVar()
Sub_Dio.set('YES')
Sub_Dio_Label = Label(lpe_frame, text=' Sub_Dio', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
Sub_Dio1 = Radiobutton(lpe_frame, text=' NO', width=7, anchor='w', variable=Sub_Dio, value='NO').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
Sub_Dio2 = Radiobutton(lpe_frame, text=' YES', width=7, anchor='w', variable=Sub_Dio, value='YES').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
COUPLING_ABS_THRESHOLD = StringVar()
COUPLING_ABS_THRESHOLD.set('1e-17')
COUPLING_REL_THRESHOLD = StringVar()
COUPLING_REL_THRESHOLD.set('0.05')
COUPLING_ABS_THRESHOLD_Label = Label(lpe_frame, text=' COUPLING_ABS', width=15, height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
COUPLING_ABS_THRESHOLD_Entry = Entry(lpe_frame, width=11, textvariable=COUPLING_ABS_THRESHOLD).grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
COUPLING_REL_THRESHOLD_Label = Label(lpe_frame, text=' COUPLING_REL', width=15, height=1, anchor='w').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
COUPLING_REL_THRESHOLD_Entry = Entry(lpe_frame, width=11, textvariable=COUPLING_REL_THRESHOLD).grid(row=basic_row, column=3, ipadx=5, ipady=5, stick=W)

# drc setting
drc_frame = Frame(run_tab)
drc_tab = run_tab.add(drc_frame,text = "DRC ",state = DISABLED)
basic_row = 0

# svs setting
svs_frame = Frame(run_tab)
svs_tab = run_tab.add(svs_frame,text = "SVS ")
basic_row = 0
Label(svs_frame, text=' Turbo', height=1, anchor='w').grid(row=0, column=0, ipadx=5, ipady=5, stick=W)
Turbo_svs = StringVar()
Turbo_svs.set('4')
Turbo_svs1= Radiobutton(svs_frame, text=' 1', width=7, anchor='w', variable=Turbo_svs, value='1').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
Turbo_svs2= Radiobutton(svs_frame, text=' 4', width=7, anchor='w', variable=Turbo_svs, value='4').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
Turbo_svs3= Radiobutton(svs_frame, text=' 8', width=7, anchor='w', variable=Turbo_svs, value='8').grid(row=basic_row, column=3, ipadx=5, ipady=5, stick=W)
Turbo_svs4 = Radiobutton(svs_frame, text=' 16', width=7, anchor='w', variable=Turbo_svs, value='16').grid(row=basic_row, column=4, ipadx=5, ipady=5, stick=W)
Turbo_svs5 = Radiobutton(svs_frame, text=' 32', width=7, anchor='w', variable=Turbo_svs, value='32').grid(row=basic_row, column=5, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
ignore_net = StringVar()
ignore_net.set('yes')
Label(svs_frame, text=' Ignore Net', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
ignore_net_mode1 = Radiobutton(svs_frame, text=' yes', width=7, anchor='w', variable=ignore_net, value='yes').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
ignore_net_mode2 = Radiobutton(svs_frame, text=' no', width=7, anchor='w', variable=ignore_net, value='no').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)
basic_row = basic_row + 1

ignore_mark = StringVar()
ignore_mark.set('yes')
Label(svs_frame, text=' Ignore Mark', height=1, anchor='w').grid(row=basic_row, column=0, ipadx=5, ipady=5, stick=W)
ignore_mark_mode1 = Radiobutton(svs_frame, text=' yes', width=7, anchor='w', variable=ignore_mark, value='yes').grid(row=basic_row, column=1, ipadx=5, ipady=5, stick=W)
ignore_mark_mode2 = Radiobutton(svs_frame, text=' no', width=7, anchor='w', variable=ignore_mark, value='no').grid(row=basic_row, column=2, ipadx=5, ipady=5, stick=W)

basic_row = basic_row + 1
ttk.Separator(svs_frame,orient='horizontal').grid(row=basic_row, columnspan=6, ipadx=5, ipady=5, stick=EW)

basic_row = basic_row + 1
svs_type1 = Label(svs_frame, text=' SVS Type1 : ', anchor='w', width=15, height=1,font=('URW Gothic L','14','bold')
