/*
///////////////////////////////////////////////////////
//  Copyright(C) ChangXin Memory Technologies, Inc.  //
//           All Rights Reserved.                    //
//                                                   //
//  Script: IMClePVPro.il                            //
//          1) Auto Stream-out/Fill-in CDL & GDS     //
//          2) PVPro-GUI for StarRC Extraction FLow  //
//          3) Also can run LVS/DRC/SVS/LVL checks   //
//  Author: Kobe Weng                                //
//                                                   //
///////////////////////////////////////////////////////
// Revision History:
// v1.0 2019/12/24 Kobe Weng
// 1) First Version of PVPro-GUI for StarRC Extraction Flow
// v1.1 2021/03/05 Leo Zhao
// 1) Force into .simrc.cdl for SHDC
// v1.2 2021/08/05 Hulda Chen
// 1) Support different projects and versions for HFDC
// v1.3 2023/02/28 pcao
// 1) Change method to recognize project site SH or HF
//      before:  use domainname 
//      after:   use CXMTutGenerateProjVerInfoList, which read  /apps/imctf/cad/runset/project_version_runset
// v1.4 2023/08/07 aaron
// 1) lowerCase(proj_name) for DBRMA
// v1.5 2023/09/21 czyang
// 1)  support lhioa (ICEM cl028kn pdk)
// 2)  use layermap when strmout 

*/

procedure( IMCleRunlpeGUI()
let( (pwdpath pathList proj_name ver libFld_Sch libFld_Lay cv cellFld_Sch cellFld_Lay runDir libName_Sch libName_Lay cdlFld rundirFld myForm fields cellName_Sch cellName_Lay gdsFld processFld metalFld)
  cv = geGetEditCellView()
  libName_Sch = cv~>libName
  cellName_Sch = cv~>cellName
  libName_Lay = cv~>libName
  cellName_Lay = cv~>cellName

;;  runDir = strcat("/proj/" getShellEnvVar("PROJ_NAME") "/" getShellEnvVar("Ver") "/ver/pex/" getShellEnvVar("USER") "/" cv~>cellName)
;;  runDir = strcat(getWorkingDir() "/ver/pex/" getShellEnvVar("USER") "/" cv~>cellName)
  pwdpath = getWorkingDir()
  pathList = parseString(pwdpath "/")
  proj_name = nth(1 pathList)
  ver = nth(2 pathList)
  runDir = strcat("/proj/" proj_name "/" ver "/ver/pex/" getShellEnvVar("USER") "/" cv~>cellName)

  libFld_Sch = hiCreateStringField(
    ?name 'mylibSch
    ?prompt "Schematic Lib Name"
    ?defValue libName_Sch
  )
  cellFld_Sch = hiCreateStringField(
    ?name 'mycellSch
    ?prompt "Schematic Cell Name"
    ?defValue cellName_Sch
  )
  libFld_Lay = hiCreateStringField(
    ?name 'mylibLay
    ?prompt "Layout Lib Name"
    ?defValue libName_Lay
  )
  cellFld_Lay = hiCreateStringField(
    ?name 'mycellLay
    ?prompt "Layout Cell Name"
    ?defValue cellName_Lay
  )
  rundirFld = hiCreateFileSelectorField(
    ?name 'myrundir
    ?prompt "Run Dir"
    ?mode 'directoryOnly
    ?defValue runDir
  )
  gdsFld = hiCreateFileSelectorField(
    ?name 'mygds
    ?prompt "Gds File"
    ?mode 'existingFile
    ?defValue strcat(runDir "/" cellName_Lay ".gds")
  )
  cdlFld = hiCreateFileSelectorField(
    ?name 'mycdl
    ?prompt "Cdl File"
    ?mode 'existingFile
    ?defValue strcat(runDir "/" cellName_Sch ".cdl")
  )
  processFld = hiCreateRadioField(
    ?name 'myprocess
    ?prompt "Process"
    ?choices list("imc19n_TX" "imc19n_RW" "imc19n_LP_RW" "cxmt10G3" "cxmt10G3_LP" "cxmt10G4" "cxmt10G4_LP" "cxmt10G5")
    ?defValue "cxmt10G3"
  )
  metalFld = hiCreateRadioField(
    ?name 'mymetal
    ?prompt "Metal"
    ?choices list("1p3m1x1y1z" "1p4m1x2y1z")
    ?defValue "1p4m1x2y1z"
  )
  fields = list(libFld_Sch cellFld_Sch libFld_Lay cellFld_Lay rundirFld gdsFld cdlFld processFld metalFld)
  myForm = hiCreateAppForm(
    ?name 'myForm
    ?fields fields
    ?formTitle "Run LPE"
    ?buttonLayout 'OKCancelApply
    ?callback "IMCleRunlpeCB(hiGetCurrentForm())"
  )
  hiDisplayForm(myForm)
)
)

procedure( IMCleRunlpeCB(myForm)
let( (runDir libName_Sch libName_Lay gdsFile lport process metal layermap cellName_Sch cellName_Lay flagList config cdlFlag cdlFile gdsFlag incFILE)
  libName_Sch = myForm~>mylibSch~>value
  cellName_Sch = myForm~>mycellSch~>value
  libName_Lay = myForm~>mylibLay~>value
  cellName_Lay = myForm~>mycellLay~>value
  runDir = myForm~>myrundir~>value
  gdsFile = myForm~>mygds~>value
  cdlFile = myForm~>mycdl~>value
  process = myForm~>myprocess~>value
  metal = myForm~>mymetal~>value
  incFILE = strcat("/apps/imctf/runset/calibre/" process "/current/common/empty_device.spi")
  layermap = strcat("/apps/imctf/libs/dfii/" process "/current/layer.map")
  unless(isDir(runDir)
    shell(strcat("mkdir -p " runDir))
  )

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;; stream out ;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  flagList = IMCleRunlpe_query(list(gdsFile cdlFile))
  gdsFlag = nth(0 flagList)
  cdlFlag = nth(1 flagList)
  when(gdsFlag == "Yes"
    printf("[INFO]: Stream out ... -%s/%s into - %s\n" libName_Lay cellName_Lay gdsFile)
    IMCleRunlpe_exportGDS(libName_Lay cellName_Lay "layout" gdsFile layermap runDir)
  )

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;; stream out ;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  when(cdlFlag == "Yes"
    printf("[INFO]: Export CDL ... -%s/%s into - %s\n" libName_Sch cellName_Sch cdlFile)
    IMCleRunlpe_exportCDL(libName_Sch cellName_Sch "schematic" cdlFile runDir incFILE)
  )
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;; Save config ;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  config = strcat(pwd() "/.lpe.config")
  lport = outfile(config)
  fprintf(lport "process = %s\n" process)
  fprintf(lport "metal = %s\n" metal)
  fprintf(lport "pex_tf = current\n")
  fprintf(lport "run_dir = %s\n" runDir)
  fprintf(lport "cdl = %s\n" cdlFile)
  fprintf(lport "cdl_top = %s\n" cellName_Sch)
  fprintf(lport "gds = %s\n" gdsFile)
  fprintf(lport "gds_top = %s\n" cellName_Lay)
  fprintf(lport "hcell = %s%s\n" runDir "/hcell")
  fprintf(lport "skip_cell = %s%s\n" runDir "/skip_cell")
  close(lport)

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;; Call pvpro ;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  system("/apps/imctf/cad/script/pvpro/pvpro.py &")
)
)

procedure( IMCleRunlpeGUI_HF()
let( (pwdpath pathList proj_name ver cv runDir libName_Sch libName_Lay viewName_Lay cdlFld 
      rundirFld schFrameField projectFld schbrs schCellField laybrs layLibField 
      schLibField layViewField process left_x top_y schViewField layFrameField 
      layCellField multi versionFld myForm fields cellName_Sch cellName_Lay viewName_Sch gdsFld processFld )
  cv = geGetEditCellView()
  case(cv~>cellViewType
    ("schematic"
        libName_Sch = cv~>libName
        cellName_Sch = cv~>cellName
        viewName_Sch = cv~>viewName 
        libName_Lay  = ""
        cellName_Lay = ""
        viewName_Lay = ""
    )
    ("maskLayout"
        libName_Sch = ""
        cellName_Sch = ""
        viewName_Sch = ""
        libName_Lay  = cv~>libName
        cellName_Lay = cv~>cellName
        viewName_Lay = cv~>viewName
    )
  )

  process = leGlobalVariables->process

  pwdpath = getWorkingDir()
  pathList = parseString(pwdpath "/")
  proj_name = nth(1 pathList)
  ver = nth(2 pathList)
  runDir = strcat("/proj/" proj_name "/" ver "/ver/pex/" getShellEnvVar("USER") "/" cv~>cellName)
  schFrameField = hiCreateFrameField(
                  ?name           'schFrameField
                  ?labelText      " Schematic input data"
                  )
  schLibField = hiCreateStringField(
            ?name           'schLibField
            ?prompt         "Library:"
            ?value          "" 
            ?defValue       libName_Sch
            ?editable       t
           )
  schCellField = hiCreateStringField(
            ?name           'schCellField
            ?prompt         "Cell:"
            ?value          ""
            ?defValue       cellName_Sch
            ?callback       "hiGetCurrentForm()~>mycdl~>value = strcat(runDir \"/\" hiGetCurrentForm()~>schCellField~>value \".cdl\")"
            ?editable       t
           )
  schViewField = hiCreateStringField(
            ?name           'schViewField
            ?prompt         "View:"
            ?value          ""
            ?defValue       viewName_Sch
            ?editable       t
           )
  schbrs = hiCreateButton(
            ?name           'schbrs
            ?buttonText     " Select cell ... "
            ?callback       "ddsSyncWithForm( hiGetCurrentForm() 'browse 'schLibField 'schCellField 'schViewField ) " 
        )
  layFrameField = hiCreateFrameField(
                  ?name           'layFrameField
                  ?labelText      " Layout input data"
                  )
  layLibField = hiCreateStringField(
            ?name           'layLibField
            ?prompt         "Library:"
            ?value          "" 
            ?defValue       libName_Lay
            ?editable       t
           )
  layCellField = hiCreateStringField(
            ?name           'layCellField
            ?prompt         "Cell:"
            ?value          ""
            ?defValue       cellName_Lay
            ?callback       "hiGetCurrentForm()~>mygds~>value = strcat(runDir \"/\" hiGetCurrentForm()~>layCellField~>value \".gds\")"
            ?editable       t
           )
  layViewField = hiCreateStringField(
            ?name           'layViewField
            ?prompt         "View:"
            ?value          ""
            ?defValue       viewName_Lay
            ?editable       t
           )
  laybrs = hiCreateButton(
            ?name           'laybrs
            ?buttonText     " Select cell ... "
            ?callback       "ddsSyncWithForm( hiGetCurrentForm() 'browse 'layLibField 'layCellField 'layViewField ) "
           )
  rundirFld = hiCreateFileSelectorField(
    ?name 'myrundir
    ?prompt "Run Dir"
    ?mode 'directoryOnly
    ?defValue runDir
  )
  gdsFld = hiCreateFileSelectorField(
    ?name 'mygds
    ?prompt "Gds File"
    ?mode 'existingFile
    ?defValue strcat(runDir "/" cellName_Lay ".gds")
  )
  cdlFld = hiCreateFileSelectorField(
    ?name 'mycdl
    ?prompt "Cdl File"
    ?mode 'existingFile
    ?defValue strcat(runDir "/" cellName_Sch ".cdl")
  )
  processFld = hiCreateRadioField(
    ?name 'myprocess
    ?prompt "Process"
    ?choices list(process)
    ?defValue process
  )
  projectFld = hiCreateRadioField(
    ?name 'myproject
    ?prompt "Project"
    ?choices list(proj_name)
    ?defValue proj_name 
  )
  versionFld = hiCreateRadioField(
    ?name 'myversion
    ?prompt "Version"
    ?choices list(ver)
    ?defValue ver 
  )
  left_x = 5
  top_y = 10
  multi = 30
  fields = list(
        list(schFrameField  left_x:top_y            800:55  10)
        list(schLibField    left_x+5:top_y+15       300:30  60)
        list(schCellField   left_x+300:top_y+15     200:30  60) 
        list(schViewField   left_x+500:top_y+15     200:30  60)  
        list(schbrs         left_x+700:top_y+15     100:30  10)      
        list(layFrameField  left_x:top_y+60         800:55  10)
        list(layLibField    left_x+5:top_y+75       300:30  60)
        list(layCellField   left_x+300:top_y+75     200:30  60) 
        list(layViewField   left_x+500:top_y+75     200:30  60)  
        list(laybrs         left_x+700:top_y+75     100:30  10)      
        list(rundirFld      left_x+5:top_y+multi*4  800:30  60)
        list(gdsFld         left_x+5:top_y+multi*5  800:30  60)
        list(cdlFld         left_x+5:top_y+multi*6  800:30  60)
        list(processFld     left_x+5:top_y+multi*7  800:30  60)  
        list(projectFld     left_x+5:top_y+multi*8  800:30  60)   
        list(versionFld     left_x+5:top_y+multi*9  800:30  60)   
        )
  myForm = hiCreateAppForm(
    ?name 'myForm
    ?fields fields
    ?formTitle "Run LPE"
    ?buttonLayout 'OKCancelApply
    ?callback "IMCleRunlpe_HFCB(hiGetCurrentForm())"
    ?initialSize t
  )
  hiDisplayForm(myForm)
)
)

procedure( IMCleRunlpe_HFCB(myForm)
let( (runDir libName_Sch cellName_Sch viewName_Sch libName_Lay cellName_Lay viewName_Lay gdsFile lport 
      process project version flagList config cdlFlag cdlFile gdsFlag incFILE layermap power_nets calibreLVS inPort 
      powernetList lvsPort calibreExtract projectList formalverList hcellFile findHcellFile)
  libName_Sch = myForm~>schLibField~>value
  cellName_Sch = myForm~>schCellField~>value
  viewName_Sch = myForm~>schViewField~>value
  libName_Lay = myForm~>layLibField~>value
  cellName_Lay = myForm~>layCellField~>value
  viewName_Lay = myForm~>layViewField~>value
  runDir = myForm~>myrundir~>value
  gdsFile = myForm~>mygds~>value
  cdlFile = myForm~>mycdl~>value
  process = myForm~>myprocess~>value
  project = myForm~>myproject~>value
  version = myForm~>myversion~>value
  incFILE = leGlobalVariables->cdlIncFile
  layermap = strcat("/apps/imctf/libs/dfii/" process "/current/layer.map")

  unless(isDir(runDir)
    shell(strcat("mkdir -p " runDir))
  )

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;; stream out ;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  flagList = IMCleRunlpe_query(list(gdsFile cdlFile))
  gdsFlag = nth(0 flagList)
  cdlFlag = nth(1 flagList)
  when(gdsFlag == "Yes"
    printf("[INFO]: Stream out ... -%s/%s into - %s\n" libName_Lay cellName_Lay gdsFile)
    IMCleRunlpe_exportGDS(libName_Lay cellName_Lay viewName_Lay gdsFile layermap runDir)
  )

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;; stream out ;;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  when(cdlFlag == "Yes"
    printf("[INFO]: Export CDL -Lib:%s Cell:%s View:%s into - %s\n" libName_Sch cellName_Sch viewName_Sch cdlFile)
    IMCleRunlpe_exportCDL(libName_Sch cellName_Sch viewName_Sch cdlFile runDir incFILE)
  )

  projectList  = CXMTutGenerateProjVerInfoList()
  ;;To get name of hcell 
  findHcellFile = sprintf(nil "/proj/%s/V0/ver/lvs/hcells" project)
  if(isFile(findHcellFile) then
    hcellFile = findHcellFile
  else
    hcellFile = "/apps/imctf/cad/script/runlpe/hcell"
  )

  ;;To get name of power_nets in calibreLVS_1p4m.extract
  formalverList = mapcar('car nthelem(2 assoc(project projectList)))
  if(member(version formalverList) then
    calibreLVS = strcat(leGlobalVariables->projRunsetPath "/current/calibreLVS.rule")
    lvsPort = infile(calibreLVS)
    while(gets(line lvsPort)
        if(index(line "calibreLVS_1p") 
            calibreExtract = cadr(parseString(line " \"\n"))
        )
    )
    close(lvsPort)
    unless(calibreExtract
         calibreExtract =calibreLVS
        )
    inPort = infile(calibreExtract)
    powernetList = list()
    while(gets(line inPort)
      if(index(line "POWER_NAME") || index(line "GROUND_NAME") then
          powernetList = append(powernetList cddr(parseString(line " \"\n")))
       )    
    )
    close(inPort)
    power_nets = buildString(artUnique(powernetList))
  else
    hiDisplayAppDBox(
        ?name 'Select_Version
        ?dboxBanner "notice window"
        ?dboxText sprintf(nil "\n[ Version:%s ]\nPlease select the project and version of pvpro afterwards !\n" version)
        ?dialogType hicInformationDialog
        ?dialogStyle 'modal
        ?buttonLayout 'Close
    )
    version = ""
    power_nets = ""
  )
  
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;; Save config ;;;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  config = strcat(runDir "/.lpe.config")
  lport = outfile(config)
  fprintf(lport "process = %s\n" process)
  fprintf(lport "project = %s\n" project)
  fprintf(lport "version = %s\n" version)
  fprintf(lport "run_dir = %s\n" runDir)
  fprintf(lport "cdl = %s\n" cdlFile)
  fprintf(lport "cdl_top = %s\n" cellName_Sch)
  fprintf(lport "gds = %s\n" gdsFile)
  fprintf(lport "gds_top = %s\n" cellName_Lay)
  fprintf(lport "hcell = %s\n" hcellFile)
  fprintf(lport "POWER_NETS = %s\n" power_nets)
  close(lport)

  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;;;;;;; Call pvpro_HF ;;;;;;;;
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  changeWorkingDir(runDir)
  system("/apps/imctf/cad/script/pvpro/pvpro.py &")
  changeWorkingDir(pwdpath)
)
)

procedure( IMCleRunlpe_exportCDL(libName_Sch cellName_Sch viewName_Sch cdlFile runDir incFILE)
let( (cdlFileFullPath cdlpathlist cdlFileName runningFile siport exportCDLcmd sienv projectList projectSite)
  cdlFileFullPath = simplifyFilename(cdlFile)
  cdlpathlist = parseString(cdlFileFullPath "/")
  cdlFileName = car(last(cdlpathlist))
  sienv = strcat(runDir "/si.env")
  siport = outfile(sienv)
  projectList  = CXMTutGenerateProjVerInfoList()
  projectSite  = nthelem(3 assoc(lowerCase(proj_name) projectList))
  fprintf(siport "simStopList = '(\"auCdl\")\n")
  fprintf(siport "simViewList = '(\"auCdl\" \"schematic\")\n")
  fprintf(siport "auCdlDefNetlistProc = \"ansCdlSubcktCall\"\n")
  fprintf(siport "globalGndSig = \"\"\n")
  fprintf(siport "globalPowerSig = \"\"\n")
  fprintf(siport "shrinkFACTOR = 0\n")
  fprintf(siport "checkScale = \"meter\"\n")
  fprintf(siport "preserveDIO = 'nil\n")
  fprintf(siport "checkDIOAREA = 'nil\n")
  fprintf(siport "checkDIOPERI = 'nil\n")
  fprintf(siport "preserveCAP = 'nil\n")
  fprintf(siport "checkCAPVAL = 'nil\n")
  fprintf(siport "checkCAPAREA = 'nil\n")
  fprintf(siport "checkCAPPERI = 'nil\n")
  fprintf(siport "preserveRES = 'nil\n")
  fprintf(siport "checkRESVAL = 'nil\n")
  fprintf(siport "checkRESSIZE ='nil\n")
  fprintf(siport "resistorModel = \"\"\n")
  fprintf(siport "shortRES = 2000\n")
  fprintf(siport "simNetlistHier = 't\n")
  fprintf(siport "pinMAP = 'nil\n")
  fprintf(siport "displayPININFO = 't\n")
  fprintf(siport "checkLDD = 'nil\n")
  fprintf(siport "incFILE = \"%s\"\n" incFILE)
  fprintf(siport "connects = \"\"\n")
  fprintf(siport "setEQUIV = \"\"\n")
  fprintf(siport "simRunDir = \"%s\"\n" runDir)
  fprintf(siport "hnlNetlistFileName = \"%s\"\n" cdlFileName)
  fprintf(siport "simSimulator = \"auCdl\"\n")
  fprintf(siport "simViewName = \"%s\"\n" viewName_Sch)
  fprintf(siport "simCellName = \"%s\"\n" cellName_Sch)
  fprintf(siport "simLibName = \"%s\"\n" libName_Sch)
  fprintf(siport "cdlSimViewList = '(\"auCdl\" \"schematic\")\n")
  fprintf(siport "cdlSimStopList = '(\"auCdl\")\n")
  close(siport)
  ;; if exist .running file, delete it
  runningFile = strcat(runDir "/.running")
  when(isFile(runningFile)  deleteFile(runningFile) )
  case(upperCase(projectSite)
      ("SH"
        if(isFile(simplifyFilename(".simrc.cdl")) then
          shell(strcat("ln -snf " simplifyFilename(".simrc.cdl") " " runDir "/.simrc"))
        else
          error("Incorrect df2 env setting, no .simrc.cdl existed, pls contact CAD")
        )
        if(isFile(simplifyFilename("cds.lib")) then
          shell(strcat("ln -snf " simplifyFilename("cds.lib") " " runDir "/cds.lib"))
        else
          error("No cds.lib existed under workdir")
        )
        exportCDLcmd = strcat("cd " runDir ";si " runDir " -batch -command netlist > " runDir "/si.log 2>&1")
        shell(exportCDLcmd)
      );;SHDC
      ("HF" 
        exportCDLcmd = strcat("si " runDir " -batch -command netlist > " runDir "/si.log 2>&1")
        shell(exportCDLcmd)
      );;HFDC
      (t
         error("Project Site - %L - don't exist!" projectSite)
       )
           
      );;case

  if( shell(strcat("grep -i '^ERROR' " runDir "/si.log")) then
    error("cdl exported failed - %s/%s, check log file - %s/si.log" libName_Sch cellName_Sch runDir)
  )
)
)

procedure(IMCleRunlpe_query(fileList)
prog( (keyword retList returnFlag)
  retList = list()
  foreach(file fileList
    if(rexMatchp("gds$" file)
      keyword = "GDS"
      keyword = "CDL"
    )
    if(isFile(file) then
      returnFlag = hiDisplayAppDBox(
        ?name 'myOverwrite
        ?dboxBanner strcat(keyword " Overwrite")
        ?dboxText strcat(file " already existed\n Do you want to overwrite it?")
        ?dialogType hicWarningDialog
        ?dialogStyle 'modal
        ?buttonLayout 'UserDefined
        ?buttons '("Yes" "No")
        ?callback '("IMCleRunlpe_overriteCB(1)" "IMCleRunlpe_overriteCB(2)")
      )
      if(returnFlag == 1
      then
        retList = append1(retList "Yes")
      else
        retList = append1(retList "No")
      )
    else
      retList = append1(retList "Yes")
    ) ;;if
  ) ;;foreach
  return(retList)
)
)

procedure( IMCleRunlpe_exportGDS(libName_Lay cellName_Lay viewName_Lay gdsFile layermap runDir)
let( (strmOutCmd)
  ;strmOutCmd=strcat("strmout -library " libName_Lay " -strmFile " gdsFile " -topCell " cellName_Lay " -view " viewName_Lay " -logFile " runDir "/strmOut.log -convertPin geometryAndText")
  strmOutCmd=strcat("strmout -library " libName_Lay " -strmFile " gdsFile " -topCell " cellName_Lay " -view " viewName_Lay  " -layerMap " layermap " -logFile " runDir "/strmOut.log -convertPin geometryAndText")
  shell(strcat("xterm -e '" strmOutCmd "'"))
;  shell(strmOutCmd)
  if( shell(strcat("grep '^ERROR' " runDir "/strmOut.log > /dev/null")) then
    error("gds exported failed -%s/%s, check log file - %s/strmOut.log" libName_Lay cellName_Lay runDir)
  )
)
)

procedure( IMCleRunlpe_overriteCB( button )
prog( ()
  when( button==1 return(1))
  when( button==2 return(2))
)
)

procedure(IMCsePullDownLay_PVPro_HF()
  let((innoMenuItem1 innoMenuItem2)
    innoMenuItem1 = hiCreateMenuItem(
      ?name      'innoLaytrim1
      ?itemText  "Stream-out"
      ?callback  "IMCleRunlpeGUI_HF()"
    )
    innoMenuItem2 = hiCreateMenuItem(
      ?name      'innoLaytrim2
      ?itemText  "No-Stream-out"
      ?callback  "system(\"/apps/imctf/cad/script/pvpro/pvpro.py &\")"
    )
    hiCreatePulldownMenu(
      'TrLayoutPulldownMenu_PVPro
      "PVPro"
      list( innoMenuItem1
            innoMenuItem2
      )
    )
  )
)

procedure( TrUserPostInstallTriggerSch_PVPro( PVPro )
if( ! member(IMCsePullDownLay_PVPro_HF()->hiMenuSym hiGetBannerMenus(PVPro->window)) then
	hiInsertBannerMenu( 
		PVPro->window 
		IMCsePullDownLay_PVPro_HF() 
		length( hiGetBannerMenus( PVPro->window ))
		)
	)
)

procedure( TrUserPostInstallTriggerLay_PVPro( PVPro )
if( ! member(IMCsePullDownLay_PVPro_HF()->hiMenuSym hiGetBannerMenus(PVPro->window)) then
	hiInsertBannerMenu( 
		PVPro->window 
		IMCsePullDownLay_PVPro_HF() 
		length( hiGetBannerMenus( PVPro->window ))
		)
	)
)

deRegUserTriggers( "schematic"
        nil
        nil
        'TrUserPostInstallTriggerSch_PVPro
        )
deRegUserTriggers( "maskLayout"
        nil
        nil
        'TrUserPostInstallTriggerLay_PVPro
        )
