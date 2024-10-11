#!/usr/bin/perl
#########################################################
################### Revsision History ###################
# v1.0  Kobe
# - initial version release
# v1.1  pcao
# - fix change format bug for diode (DD)
# v1.2  pcao 2023/09/04
# - add LayerINFO and REDUCTION conflict check
# v1.3  Shanshan
# - add lpe_star option
# v1.4  pcao
# - add check for skip cell must exist in hcell check, if not, will exit
# v1.5  Wens
# - print the missed options
# v1.6  ssfang
# - add 3D_IC option, only support on R/RC/RCC
#########################################################
#use warnings;
use Cwd;
use Cwd 'abs_path';
use Getopt::Long;
use Term::ANSIColor;
use File::Basename;

##options for user
my @optname;
my $missopt;
our $opt_config = "";
our $opt_help;
GetOptions('config=s', 'help');

if(($opt_config eq "") || ($opt_help)) {
  help();
}

$lpe_star = "lpe_star";

#################
## main script ##
#################
open(CONFIG,"<$opt_config") || die "[", color("red", color("reset"), "] Cannot open lpe.config\n");
  while(<CONFIG>) {
    $process = $1 if /^\s*process\s*=\s*(\S+)/i;
    $project = $1 if /^\s*project\s*=\s*(\S+)/i;
    $version = lc $1 if /^\s*version\s*=\s*(\S+)/i;
    $lpe_star = $1 if /^\s*lpe_star\s*=\s*(\S+)/i;
    $pex_tf = $1 if /^\s*pex_tf\s*=\s*(\S+)/i;
    $source = $1 if /^\s*(?:cdl|source)\s*=\s*(\S+)/i;
    $source_top = $1 if /^\s*(?:cdl_top|source_top)\s*=\s*(\S+)/i;
    $gds = $1 if /^\s*gds\s*=\s*(\S+)/i;
    $gds_top = $1 if /^\s*gds_top\s*=\s*(\S+)/i;
    $mode = $1 if /^\s*mode\s*=\s*(\S+)/i;
    $threeD_IC = $1 if /^\s*3D_IC\s*=\s*(\S+)/i;
    $hcell = $1 if /^\s*hcell\s*=\s*(\S+)/i;
    $skip_cell = $1 if /^\s*skip_cell\s*=\s*(\S+)/i;
    $virtual_connect = $1 if /^\s*VIRTUAL_CONNECT\s*=\s*(\S+)/i;
    $select_nets = $1 if /^\s*NETS\s*=\s*(.*)/i;
    $netlist_type = $1 if /^\s*PG_Ronly_NETS\s*=\s*(.*)/i;
    $netlist_instance_section = $1 if /^\s*NETLIST_INSTANCE_SECTION\s*=\s*(.*)/i;
    $net_type = $1 if /^\s*NET_TYPE\s*=\s*(\S+)/i;
    $cell_type = $1 if /^\s*CELL_TYPE\s*=\s*(\S+)/i;
    $power_extract = $1 if /^\s*POWER_EXTRACT\s*=\s*(\S+)/i;
    $power_nets = $1 if /^\s*POWER_NETS\s*=\s*(.*)/i;
    $Keep_Power = $1 if /^\s*Keep_Power\s*=\s*(.*)/i;
    $device_coordinate = $1 if /^\s*DEVICE_COORDINATE\s*=\s*(\S+)/i;
    $placement_info = $1 if /^\s*PLACEMENT_INFO_FILE\s*=\s*(\S+)/i;
    $reduction = $1 if /^\s*REDUCTION\s*=\s*(\S+)/i;
    $coupling_abs_threshold = $1 if /^\s*COUPLING_ABS_THRESHOLD\s*=\s*(\S+)/i;
    $coupling_rel_threshold = $1 if /^\s*COUPLING_REL_THRESHOLD\s*=\s*(\S+)/i;
    $floating_as_fill = $1 if /^\s*FLOATING_AS_FILL\s*=\s*(\S+)/i;
    $hierarchical_separator = $1 if /^\s*HIERARCHICAL_SEPARATOR\s*=\s*(\S+)/i;
    $netlist_nodename_netname = $1 if /^\s*NETLIST_NODENAME_NETNAME\s*=\s*(\S+)/i;
    $change_device_format = $1 if /^\s*CHANGE_DEVICE_FORMAT\s*=\s*(\S+)/i;
    $netlist_subckt = $1 if /^\s*NETLIST_SUBCKT\s*=\s*(\S+)/i;
    $r3d = $1 if /^\s*R3D\s*=\s*(\S+)/i;
    $lpe_lvs = $1 if /^\s*CHK_LPE_LVS\s*=\s*(\S+)/i;
    $Sub_Dio = $1 if /^\s*Sub_Dio\s*=\s*(\S+)/i;
    $spres = $1 if /^\s*SPRES\s*=\s*(\S+)/i;
    $totem = $1 if /^\s*TOTEM\s*=\s*(\S+)/i;
    $LayerINFO = $1 if /^\s*LayerINFO\s*=\s*(\S+)/i;
    $ba_diode = $1 if /^\s*BA_Diode\s*=\s*(\S+)/i;
    $Core_Num = $1 if /^\s*Core_Num\s*=\s*(\S+)/i;
    $Cap_Rep = $1 if /^\s*Cap_Rep\s*=\s*(\S+)/i;
    $bulk = $1 if /^\s*BULK\s*=\s*(\S+)/i;
}

close CONFIG;

#Check lpe.config setting
#NOTE: if add/delete options, MUST edit @option & @optName at the same time
my @option = ($process, $project, $version, $lpe_star, $pex_tf, $source, $source_top, $gds, $gds_top, $mode, $threeD_IC, $hcell, $skip_cell, $virtual_connect, $select_nets, $netlist_instance_section, $net_type, $cell_type, $power_extract, $power_nets, $Keep_Power, $device_coordinate, $placement_info, $reduction, $coupling_abs_threshold, $coupling_rel_threshold, $floating_as_fill, $hierarchical_separator, $netlist_nodename_netname, $change_device_format, $netlist_subckt, $r3d, $lpe_lvs, $Sub_Dio, $spres, $totem,$LayerINFO, $ba_diode, $Core_Num, $Cap_Rep, $bulk);
my @optName = ("process", "project", "version", "lpe_star", "pex_tf", "cdl", "cdl_top", "gds", "gds_top", "mode", "3D_IC", "hcell", "skip_cell", "VIRTUAL_CONNECT", "NETS", "NETLIST_INSTANCE_SECTION", "NET_TYPE", "CELL_TYPE", "POWER_EXTRACT", "POWER_NETS", "Keep_Power", "DEVICE_COORDINATE", "PLACEMENT_INFO_FILE", "REDUCTION", "COUPLING_ABS_THRESHOLD", "COUPLING_REL_THRESHOLD", "FLOATING_AS_FILL", "HIERARCHICAL_SEPARATOR", "NETLIST_NODENAME_NETNAME", "CHANGE_DEVICE_FORMAT", "NETLIST_SUBCKT", "R3D", "CHK_LPE_LVS", "Sub_Dio", "SPRES", "TOTEM", "LayerINFO", "BA_Diode", "Core_Num", "Cap_Rep", "BULK");
check_config(\@option, \@optName); 

###### pcao add LayerINFO and reduction confilct check, 2023-09-04
if(($LayerINFO eq "YES") && ($reduction eq "YES" || $reduction eq "HIGH" || $reduction eq "NO_EXTRA_LOOPS") ) {
    print "\nLayerINFO:$LayerINFO and REDUCTION:$reduction are confilct\n";
    print "Only REDUCTION:NO|LAYER|LAYER_NO_EXTRA_LOOPS can be set when LayerINFO:YES is used in a RC extraction run \n\n";
    exit();
}
if($pex_tf ne "current") {
  my $pex_tf = "/apps/imctf/runset/starrc/$process/data/$pex_tf/tf";
  if(-e $pex_tf) {
    print "\nPEX-TF version is $pex_tf";
  }
  else {
    print "$pex_tf\n";
    print "\nPEX-TF path is incorrect!!\n\n";
    exit();
  }
}

if(-e $skip_cell) {
  open(SKIP_CELL,"<$skip_cell") || die "[", color("red", color("reset"), "] Cannot open $skip_cell\n");
    foreach $line(<SKIP_CELL>) {
      if($line =~ m/(\S+)/) {
        push @skip_cells , $1;
      }
  }
  close SKIP_CELL;
}

print "skip cells: @skip_cells\n\n";
###### pcao add skip cell must exist in hcell check, 2023-09-25
if(-e $hcell) {
  open(HCELL,"<$hcell") || die "[", color("red", color("reset"), "] Cannot open $hcell\n");
    foreach $line(<HCELL>) {
      if($line =~ m/(^[^#\/\\]+\S+)\s+(\S+)/) {
        push @hcells , $2;
      }
  }
  close HCELL;
}

#print "@hcells \n";
my $err_flag = 0;
foreach $tmp_skip_cell(@skip_cells) {
    if ( not grep { $tmp_skip_cell eq $_ } @hcells) {
        $err_flag = $err_flag + 1;
        print "[ERROR]: skip cell $tmp_skip_cell is NOT in the hcell list\n";
    }  
}

if($err_flag)  {
    print "\nPlease check below errors at first!! \n\n";
    exit();
}


my $calibreLPErule = "/apps/imctf/cad/runset/$project/$version/current/$lpe_star/calibreLPE.rule";
if(-e $calibreLPErule) {
  open(RUNSET,"<$calibreLPErule") || die "[", color("red", color("reset"), "] Cannot open calibreLPE.rule\n");
  @file = <RUNSET>;
  close RUNSET;
}
else {
  print "Project \"$project\" or Version Option \"$version\" is not supported !!\n";
  exit();
}

open(RUNSET, ">lpe_$mode.rule") || die "[", color("red", color("reset"), "] Cannot open lpe_$mode}.rule\n");
  foreach $line(@file) {
    $line =~ s/LAYOUT PATH ".\/layout.gds"/LAYOUT PATH "$gds"/g;
    $line =~ s/LAYOUT PRIMARY "layout_top"/LAYOUT PRIMARY "$gds_top"/g;
    $line =~ s/SOURCE PATH ".\/source.spi"/SOURCE PATH "$source"/g;
    $line =~ s/SOURCE PRIMARY "source_top"/SOURCE PRIMARY "$source_top"/g;
    if($virtual_connect eq "YES") {
      $line =~ s/\/\/VIRTUAL CONNECT COLON YES/VIRTUAL CONNECT COLON YES/g;
      $line =~ s/\/\/VIRTUAL CONNECT NAME \?/VIRTUAL CONNECT NAME \?/g;
    }
    if($Sub_Dio eq "NO") {
      $line =~ s/#DEFINE extract_subdio/\/\/#DEFINE extract_subdio/g;
    }
    if($power_extract eq "YES") {
      $line =~ s/LVS POWER NAME POWER_NAME/\/\/LVS POWER NAME POWER_NAME/g;
      $line =~ s/LVS GROUND NAME GROUND_NAME/\/\/LVS GROUND NAME GROUND_NAME/g;
    }
    print RUNSET $line;
  }
close RUNSET;

system("rm -rf svdb CCI_DB");

##run LVS
system("calibre -lvs -spice layout.spi -hier -turbo $Core_Num -hcell $hcell lpe_$mode.rule | tee cci_lvs.log");

if(($lpe_lvs eq NO) || ($spres eq YES)) {
  print "\nDon't Check LVS Result!!\n\n";
}
else {
  open(LVS_REP, "<cci_lvs.log") || die "[", color("red", color("reset"), "] Cannot open cci_lvs.log\n");
  while(<LVS_REP>) {
    if((/LVS completed\. NOT COMPARED\./) || (/LVS completed\. INCORRECT\./)) {
      print "\n Terminate LPE running due to CCI-LVS result is NOT Clean !!\n\n";
      system("xmessage -center 'Sorry! Cell \"$gds_top\" Run LVS Failed!' &");
      exit();
    }
  }
  close LVS_REP;
}

##run query_cmd
system("cp /apps/imctf/cad/runset/$project/$version/current/$lpe_star/query_cmd .");

system("mkdir CCI_DB");
system("calibre -64 -query_input query_cmd -query svdb | tee cci_query.log");

##run StarRC
#open(STAR_CMD,"</apps/imctf/cad/runset/$project/$version/current/$lpe_star/star_cmd") || die "[", color("red", color("reset"), "] Cannot open star_cmd\n");
open(STAR_CMD,"</home/cad1/ssfang/python/pvpro/script/star_cmd") || die "[", color("red", color("reset"), "] Cannot open star_cmd\n");
  @file = <STAR_CMD>;
close STAR_CMD;

#check mode and star_cmd that is not support for 3D_IC.
my $threeD_cmd1, $threeD_cmd2, $threeD_cmd3;
if($threeD_IC eq YES) {
  if(($mode eq CC) || ($mode eq C)) {
    print "\n 3D_IC is not supported on CC\/C mode !\n\n";
    exit();
  } else {
    #open(STAR_CMD,"</apps/imctf/cad/runset/$project/$version/current/$lpe_star/star_cmd") || die "[", color("red", color("reset"), "] Cannot open star_cmd\n");
    open(STAR_CMD,"</home/cad1/ssfang/python/pvpro/script/star_cmd") || die "[", color("red", color("reset"), "] Cannot open star_cmd\n");
      while(<STAR_CMD>) {
        $threeD_cmd1 = $1 if /^\s*3D_IC\s*:\s*(\S+)/i;
        $threeD_cmd2 = $1 if /^\s*3D_IC_TSV_COUPLING_EXTRACTION\s*:\s*(\S+)/i;
        $threeD_cmd3 = $1 if /^\s*3D_IC_SUBCKT_FILE\s*:\s*(\S+)/i;
      }
    close STAR_CMD;
    print "\n$threeD_cmd1\n$threeD_cmd2\n$threeD_cmd3\n";
    if((!$threeD_cmd1) || (!$threeD_cmd2) || (!$threeD_cmd3)) {
      print "\nThe star_cmd file of $project is not supported for 3D_IC !\n\n";
      exit();
    }
  }
}

open(STAR_CMD, ">star_cmd_$mode") || die "[", color("red", color("reset"), "] Cannot open star_cmd\n");
  foreach $line(@file) {
    if($mode eq CC) {
      if($cell_type eq SCHEMATIC) {
        $line =~ s/BLOCK:\s*top_cell/BLOCK: $source_top/g;
      } else {
        $line =~ s/BLOCK:\s*top_cell/BLOCK: $gds_top/g;
      }
      $line =~ s/CALIBRE_RUNSET:\s*lpe_deck/CALIBRE_RUNSET: lpe_$mode.rule/g;
      if($pex_tf ne current) {
        $line =~ s/TCAD_GRD_FILE: \/apps\/imctf\/runset\/starrc\/$process\/data\/(\S+)\/tf\/(\S+)/TCAD_GRD_FILE: \/apps\/imctf\/runset\/starrc\/$process\/data\/$pex_tf\/tf\/$2/g;
      }
      $line =~ s/EXTRACTION:\s*RC/EXTRACTION: C/g;
      $line =~ s/^\s*3D_IC:\s*\S*/3D_IC: NO/g;
      $line =~ s/HIERARCHICAL_SEPARATOR:\s*\//HIERARCHICAL_SEPARATOR: $hierarchical_separator/g;
      $line =~ s/NETLIST_NODENAME_NETNAME:\s*NO/NETLIST_NODENAME_NETNAME: $netlist_nodename_netname/g;
      $line =~ s/COUPLE_TO_GROUND:\s*YES/COUPLE_TO_GROUND: NO/g;
      $line =~ s/SPICE_SUBCKT_FILE:\s*spice_subckt_file/SPICE_SUBCKT_FILE: $source/g;
      $line =~ s/^\s*NETS:\s*\*/NETS: $select_nets/g;
      $line =~ s/^\s*NETLIST_TYPE:\s*R/NETLIST_TYPE: no_couple R $netlist_type/g;
      $line =~ s/NETLIST_INSTANCE_SECTION:\s*SELECTED/NETLIST_INSTANCE_SECTION: $netlist_instance_section/g;
      $line =~ s/NETLIST_SUBCKT:\s*YES/NETLIST_SUBCKT: $netlist_subckt/g;
      $line =~ s/NET_TYPE:\s*LAYOUT/NET_TYPE: $net_type/g;
      $line =~ s/CELL_TYPE:\s*LAYOUT/CELL_TYPE: $cell_type/g;
      if($power_extract eq LRSD) {
        $line =~ s/POWER_EXTRACT:\s*NO/POWER_EXTRACT: DEVICE_LAYERS/g;
      } else {
        $line =~ s/POWER_EXTRACT:\s*NO/POWER_EXTRACT: $power_extract/g;
      }
      $line =~ s/POWER_NETS:\s*power_nets/POWER_NETS: $power_nets/g;
      $line =~ s/SKIP_CELLS:\s*skip_cells/SKIP_CELLS: !* @skip_cells/g;
      if($totem eq YES) {
        $line =~ s/NETLIST_DEVICE_LOCATION_ORIENTATION:\s*NO/NETLIST_DEVICE_LOCATION_ORIENTATION: YES/g;
      } else {
        $line =~ s/NETLIST_DEVICE_LOCATION_ORIENTATION:\s*NO/NETLIST_DEVICE_LOCATION_ORIENTATION: $device_coordinate/g;
      }
      $line =~ s/PLACEMENT_INFO_FILE:\s*NO/PLACEMENT_INFO_FILE: $placement_info/g;
      $line =~ s/REDUCTION:\s*NO/REDUCTION: $reduction/g;
      $line =~ s/COUPLING_ABS_THRESHOLD:\s*1e-17/COUPLING_ABS_THRESHOLD: $coupling_abs_threshold/g;
      $line =~ s/COUPLING_REL_THRESHOLD:\s*0.05/COUPLING_REL_THRESHOLD: $coupling_rel_threshold/g;
      $line =~ s/TRANSLATE_FLOATING_AS_FILL:\s*YES/TRANSLATE_FLOATING_AS_FILL: $floating_as_fill/g;
      $line =~ s/TRANSLATE_RETAIN_BULK_LAYERS:\s*YES/TRANSLATE_RETAIN_BULK_LAYERS: $bulk/g;
      if($r3d eq YES) {
        $line =~ s/NUM_CORES: 8\s*/NUM_CORES: 8\n\nFSCOMPARE_THRESHOLD: 1e-20\nFSCOMPARE_COUPLING_THRESHOLD: 1e-20\nFSCOMPARE_COUPLING_RATIO: 0.001\nFS_EXTRACT_NETS: *\n\n/g;
      }
      print STAR_CMD $line;
    }
    elsif($mode eq RCC) {
      if($cell_type eq SCHEMATIC) {
        $line =~ s/BLOCK:\s*top_cell/BLOCK: $source_top/g;
      } else {
        $line =~ s/BLOCK:\s*top_cell/BLOCK: $gds_top/g;
      }
      $line =~ s/CALIBRE_RUNSET:\s*lpe_deck/CALIBRE_RUNSET: lpe_$mode.rule/g;
      if($pex_tf ne current) {
        $line =~ s/TCAD_GRD_FILE: \/apps\/imctf\/runset\/starrc\/$process\/data\/(\S+)\/tf\/(\S+)/TCAD_GRD_FILE: \/apps\/imctf\/runset\/starrc\/$process\/data\/$pex_tf\/tf\/$2/g;
      }
      $line =~ s/^\s*3D_IC:\s*\S*/3D_IC: $threeD_IC/g;
      $line =~ s/HIERARCHICAL_SEPARATOR:\s*\//HIERARCHICAL_SEPARATOR: $hierarchical_separator/g;
      $line =~ s/NETLIST_NODENAME_NETNAME:\s*NO/NETLIST_NODENAME_NETNAME: $netlist_nodename_netname/g;
      $line =~ s/COUPLE_TO_GROUND:\s*YES/COUPLE_TO_GROUND: NO/g;
      $line =~ s/SPICE_SUBCKT_FILE:\s*spice_subckt_file/SPICE_SUBCKT_FILE: $source/g;
      $line =~ s/^\s*NETS:\s*\*/NETS: $select_nets/g;
      $line =~ s/^\s*NETLIST_TYPE:\s*R/NETLIST_TYPE: no_couple R $netlist_type/g;
      $line =~ s/NETLIST_INSTANCE_SECTION:\s*SELECTED/NETLIST_INSTANCE_SECTION: $netlist_instance_section/g;
      $line =~ s/NETLIST_SUBCKT:\s*YES/NETLIST_SUBCKT: $netlist_subckt/g;
      $line =~ s/NET_TYPE:\s*LAYOUT/NET_TYPE: $net_type/g;
      $line =~ s/CELL_TYPE:\s*LAYOUT/CELL_TYPE: $cell_type/g;
      if($power_extract eq LRSD) {
        $line =~ s/POWER_EXTRACT:\s*NO/POWER_EXTRACT: DEVICE_LAYERS/g;
      } else {
        $line =~ s/POWER_EXTRACT:\s*NO/POWER_EXTRACT: $power_extract/g;
      }
      $line =~ s/POWER_NETS:\s*power_nets/POWER_NETS: $power_nets/g;
      $line =~ s/SKIP_CELLS:\s*skip_cells/SKIP_CELLS: !* @skip_cells/g;
      if($totem eq YES) {
        $line =~ s/NETLIST_DEVICE_LOCATION_ORIENTATION:\s*NO/NETLIST_DEVICE_LOCATION_ORIENTATION: YES/g;
      } else {
        $line =~ s/NETLIST_DEVICE_LOCATION_ORIENTATION:\s*NO/NETLIST_DEVICE_LOCATION_ORIENTATION: $device_coordinate/g;
      }
      $line =~ s/PLACEMENT_INFO_FILE:\s*NO/PLACEMENT_INFO_FILE: $placement_info/g;
      $line =~ s/REDUCTION:\s*NO/REDUCTION: $reduction/g;
      $line =~ s/COUPLING_ABS_THRESHOLD:\s*1e-17/COUPLING_ABS_THRESHOLD: $coupling_abs_threshold/g;
      $line =~ s/COUPLING_REL_THRESHOLD:\s*0.05/COUPLING_REL_THRESHOLD: $coupling_rel_threshold/g;
      $line =~ s/TRANSLATE_FLOATING_AS_FILL:\s*YES/TRANSLATE_FLOATING_AS_FILL: $floating_as_fill/g;
      $line =~ s/TRANSLATE_RETAIN_BULK_LAYERS:\s*YES/TRANSLATE_RETAIN_BULK_LAYERS: $bulk/g;
      if($r3d eq YES) {
        $line =~ s/NUM_CORES: 8\s*/NUM_CORES: 8\n\nFSCOMPARE_THRESHOLD: 1e-20\nFSCOMPARE_COUPLING_THRESHOLD: 1e-20\nFSCOMPARE_COUPLING_RATIO: 0.001\nFS_EXTRACT_NETS: *\n\n/g;
      }
      print STAR_CMD $line;
    }
    elsif(($mode eq R) || ($mode eq C) || ($mode eq RC)) {
      if($cell_type eq SCHEMATIC) {
        $line =~ s/BLOCK:\s*top_cell/BLOCK: $source_top/g;
      } else {
        $line =~ s/BLOCK:\s*top_cell/BLOCK: $gds_top/g;
      }
      $line =~ s/CALIBRE_RUNSET:\s*lpe_deck/CALIBRE_RUNSET: lpe_$mode.rule/g;
      if($pex_tf ne current) {
        $line =~ s/TCAD_GRD_FILE: \/apps\/imctf\/runset\/starrc\/$process\/data\/(\S+)\/tf\/(\S+)/TCAD_GRD_FILE: \/apps\/imctf\/runset\/starrc\/$process\/data\/$pex_tf\/tf\/$2/g;
      }
      $line =~ s/EXTRACTION:\s*RC/EXTRACTION: $mode/g;
      $line =~ s/^\s*3D_IC:\s*\S*/3D_IC: $threeD_IC/g;
      $line =~ s/HIERARCHICAL_SEPARATOR:\s*\//HIERARCHICAL_SEPARATOR: $hierarchical_separator/g;
      $line =~ s/NETLIST_NODENAME_NETNAME:\s*NO/NETLIST_NODENAME_NETNAME: $netlist_nodename_netname/g;
      $line =~ s/NETLIST_SUBCKT:\s*YES/NETLIST_SUBCKT: $netlist_subckt/g;
      $line =~ s/SPICE_SUBCKT_FILE:\s*spice_subckt_file/SPICE_SUBCKT_FILE: $source/g;
      $line =~ s/^\s*NETS:\s*\*/NETS: $select_nets/g;
      $line =~ s/^\s*NETLIST_TYPE:\s*R/NETLIST_TYPE: no_couple R $netlist_type/g;
      $line =~ s/NETLIST_INSTANCE_SECTION:\s*SELECTED/NETLIST_INSTANCE_SECTION: $netlist_instance_section/g;
      $line =~ s/NET_TYPE:\s*LAYOUT/NET_TYPE: $net_type/g;
      $line =~ s/CELL_TYPE:\s*LAYOUT/CELL_TYPE: $cell_type/g;
      if($power_extract eq LRSD) {
        $line =~ s/POWER_EXTRACT:\s*NO/POWER_EXTRACT: DEVICE_LAYERS/g;
      } else {
        $line =~ s/POWER_EXTRACT:\s*NO/POWER_EXTRACT: $power_extract/g;
      }
      $line =~ s/POWER_NETS:\s*power_nets/POWER_NETS: $power_nets/g;
      $line =~ s/SKIP_CELLS:\s*skip_cells/SKIP_CELLS: !* @skip_cells/g;
      if($totem eq YES) {
        $line =~ s/NETLIST_DEVICE_LOCATION_ORIENTATION:\s*NO/NETLIST_DEVICE_LOCATION_ORIENTATION: YES/g;
      } else {
        $line =~ s/NETLIST_DEVICE_LOCATION_ORIENTATION:\s*NO/NETLIST_DEVICE_LOCATION_ORIENTATION: $device_coordinate/g;
      }
      $line =~ s/PLACEMENT_INFO_FILE:\s*NO/PLACEMENT_INFO_FILE: $placement_info/g;
      $line =~ s/REDUCTION:\s*NO/REDUCTION: $reduction/g;
      $line =~ s/COUPLING_ABS_THRESHOLD:\s*1e-17/COUPLING_ABS_THRESHOLD: $coupling_abs_threshold/g;
      $line =~ s/COUPLING_REL_THRESHOLD:\s*0.05/COUPLING_REL_THRESHOLD: $coupling_rel_threshold/g;
      $line =~ s/TRANSLATE_FLOATING_AS_FILL:\s*YES/TRANSLATE_FLOATING_AS_FILL: $floating_as_fill/g;
      $line =~ s/TRANSLATE_RETAIN_BULK_LAYERS:\s*YES/TRANSLATE_RETAIN_BULK_LAYERS: $bulk/g;
      if($r3d eq YES) {
        $line =~ s/NUM_CORES: 8\s*/NUM_CORES: 8\n\nFSCOMPARE_THRESHOLD: 1e-20\nFSCOMPARE_COUPLING_THRESHOLD: 1e-20\nFSCOMPARE_COUPLING_RATIO: 0.001\nFS_EXTRACT_NETS: *\n\n/g;
      }
      print STAR_CMD $line;
    }
    elsif($mode eq FSCOMPARE) {
      if($cell_type eq SCHEMATIC) {
        $line =~ s/BLOCK:\s*top_cell/BLOCK: $source_top/g;
      } else {
        $line =~ s/BLOCK:\s*top_cell/BLOCK: $gds_top/g;
      }
      $line =~ s/CALIBRE_RUNSET:\s*lpe_deck/CALIBRE_RUNSET: lpe_$mode.rule/g;
      if($pex_tf ne current) {
        $line =~ s/TCAD_GRD_FILE: \/apps\/imctf\/runset\/starrc\/$process\/data\/(\S+)\/tf\/(\S+)/TCAD_GRD_FILE: \/apps\/imctf\/runset\/starrc\/$process\/data\/$pex_tf\/tf\/$2/g;
      }
      $line =~ s/EXTRACTION:\s*RC/EXTRACTION: $mode/g;
      $line =~ s/^\s*3D_IC:\s*\S*/3D_IC: NO/g;
      $line =~ s/HIERARCHICAL_SEPARATOR:\s*\//HIERARCHICAL_SEPARATOR: $hierarchical_separator/g;
      $line =~ s/NETLIST_NODENAME_NETNAME:\s*NO/NETLIST_NODENAME_NETNAME: $netlist_nodename_netname/g;
      $line =~ s/NETLIST_SUBCKT:\s*YES/NETLIST_SUBCKT: $netlist_subckt/g;
      $line =~ s/SPICE_SUBCKT_FILE:\s*spice_subckt_file/SPICE_SUBCKT_FILE: $source/g;
      $line =~ s/^\s*NETS:\s*\*/NETS: $select_nets/g;
      $line =~ s/^\s*NETLIST_TYPE:\s*R/NETLIST_TYPE: no_couple R $netlist_type/g;
      $line =~ s/NETLIST_INSTANCE_SECTION:\s*SELECTED/NETLIST_INSTANCE_SECTION: $netlist_instance_section/g;
      $line =~ s/NET_TYPE:\s*LAYOUT/NET_TYPE: $net_type/g;
      $line =~ s/CELL_TYPE:\s*LAYOUT/CELL_TYPE: $cell_type/g;
      if($power_extract eq LRSD) {
        $line =~ s/POWER_EXTRACT:\s*NO/POWER_EXTRACT: DEVICE_LAYERS/g;
      } else {
        $line =~ s/POWER_EXTRACT:\s*NO/POWER_EXTRACT: $power_extract/g;
      }
      $line =~ s/POWER_NETS:\s*power_nets/POWER_NETS: $power_nets/g;
      $line =~ s/SKIP_CELLS:\s*skip_cells/SKIP_CELLS: !* @skip_cells/g;
      if($totem eq YES) {
        $line =~ s/NETLIST_DEVICE_LOCATION_ORIENTATION:\s*NO/NETLIST_DEVICE_LOCATION_ORIENTATION: YES/g;
      } else {
        $line =~ s/NETLIST_DEVICE_LOCATION_ORIENTATION:\s*NO/NETLIST_DEVICE_LOCATION_ORIENTATION: $device_coordinate/g;
      }
      $line =~ s/PLACEMENT_INFO_FILE:\s*NO/PLACEMENT_INFO_FILE: $placement_info/g;
      $line =~ s/REDUCTION:\s*NO/REDUCTION: $reduction/g;
      $line =~ s/COUPLING_ABS_THRESHOLD:\s*1e-17/COUPLING_ABS_THRESHOLD: $coupling_abs_threshold/g;
      $line =~ s/COUPLING_REL_THRESHOLD:\s*0.05/COUPLING_REL_THRESHOLD: $coupling_rel_threshold/g;
      $line =~ s/TRANSLATE_FLOATING_AS_FILL:\s*YES/TRANSLATE_FLOATING_AS_FILL: $floating_as_fill/g;
      $line =~ s/TRANSLATE_RETAIN_BULK_LAYERS:\s*YES/TRANSLATE_RETAIN_BULK_LAYERS: $bulk/g;
      $line =~ s/NUM_CORES: 8\s*/NUM_CORES: 8\n\nFSCOMPARE_THRESHOLD: 1e-20\nFSCOMPARE_COUPLING_THRESHOLD: 1e-20\nFSCOMPARE_COUPLING_RATIO: 0.001\n\n/g;
      print STAR_CMD $line;
    }
    else {
      print "You choose wrong RC mode!!\n";
    }
  }
  if($spres eq YES) {
    print STAR_CMD "NETLIST_TAIL_COMMENTS: YES\nEXTRA_GEOMETRY_INFO: RES NODE\n";
    print STAR_CMD "NETLIST_CONNECT_SECTION: YES\nNETLIST_NODE_SECTION: YES\nSHORT_PINS: NO\n";
    print STAR_CMD "XREF: NO\n";
  }

  if($totem eq YES) {
    print STAR_CMD "NETLIST_IDEAL_SPICE_FILE: ideal.netlist\n";
    print STAR_CMD "STAR_DIRECTORY: STAR\n";
    print STAR_CMD "NETLIST_CONNECT_SECTION: YES\n";
    print STAR_CMD "NETLIST_NODE_SECTION: YES\n";
    print STAR_CMD "NETLIST_TAIL_COMMENTS: YES\n";
    print STAR_CMD "NETLIST_NAME_MAP: YES\n";
    print STAR_CMD "NETLIST_IDEAL_SPICE_TYPE: LAYOUT\n";
    print STAR_CMD "MODEL_TYPE: LAYOUT\n";
    print STAR_CMD "AUTO_RUNSET: YES\n";
    print STAR_CMD "NETLIST_COMMENTED_PARAMS: YES\n";
    print STAR_CMD "EXTRA_GEOMETRY_INFO: NODE\n";
    print STAR_CMD "SHORT_PINS: NO\n";
  }

  if($LayerINFO eq YES) {
    print STAR_CMD "NETLIST_TAIL_COMMENTS: YES\n";
    print STAR_CMD "CAPACITOR_TAIL_COMMENTS: YES\n";
    print STAR_CMD "EXTRA_GEOMETRY_INFO: RES NODE\n";
    print STAR_CMD "KEEP_VIA_NODES: YES\n";
    print STAR_CMD "NETLIST_DEVICE_LOCATION_ORIENTATION: YES\n";
    print STAR_CMD "NETLIST_NODE_SECTION: YES\n";
   }

  if($Core_Num ne 1) {
    print STAR_CMD "STARRC_DP_STRING: list localhost:$Core_Num\n";
  }

close STAR_CMD;

#Post-process star_cmd
if(($Keep_Power ne "") && ($Keep_Power ne ALL) && ($power_extract eq YES)) {
  open(STAR_CMD,"< star_cmd_$mode") || die "[", color("red", color("reset"), "] Cannot open star_cmd_$mode\n");
    @file = <STAR_CMD>;
  close STAR_CMD;

  $power_nets =~ s/\*/StarRC/g;
  $Keep_Power =~ s/\*/StarRC/g;

  foreach my $line(split(/\s+/, $power_nets)) {
    if(not grep /$line/, $Keep_Power) {
      $line =~ s/StarRC/*/g;
      push @Special_NET, "!$line";
    }
  }

  open(STAR_CMD,"> star_cmd_$mode") || die "[", color("red", color("reset"), "] Cannot open star_cmd_$mode\n");
    foreach my $line(@file) {
      $line =~ s/^\s*NETS:\s*\*/NETS: * @Special_NET/g;
      print STAR_CMD $line;
    }
  close STAR_CMD;
}

#Run StarRC Extraction
system("StarXtract -clean star_cmd_$mode");

system("mv $gds_top.spf $gds_top.spf_$mode");

#Post-process LPE netlist

if($process eq imc19n_TX) {
  print"Post-process LPE netlist ...\n";
  open(SPF, "< $gds_top.spf_$mode") || die "[", color("red", color("reset"), "] Cannot open $gds_top.spf_$mode\n");
    @file = <SPF>;
  close SPF;

  open(SPF, "> $gds_top.spf_$mode") or die "[", color("red", color("reset"), "] Cannot open $gds_top.spf_$mode\n");
    foreach my $line(@file) {
      $line =~ s/\sRESNM\s/ /g;
      $line =~ s/\sRESN\s/ /g;
      $line =~ s/\sRESGP\s/ /g;
      $line =~ s/\sRESM1\s/ /g;
      $line =~ s/\sRESM2\s/ /g;
      $line =~ s/\sRESM3\s/ /g;
      $line =~ s/\sRESM4\s/ /g;
      $line =~ s/\sRESM2OFF\s/ /g;
      $line =~ s/\sRESM3OFF\s/ /g;
      $line =~ s/\sRESM4OFF\s/ /g;
      $line =~ s/\sFUSE\s/ /g;
      $line =~ s/\sCAPCYL\s/ /g;
      print SPF $line;
  }
  close SPF;
}
elsif($process eq imc19n_RW) {
  print"Post-process LPE netlist ...\n";
  open(SPF, "< $gds_top.spf_$mode") || die "[", color("red", color("reset"), "] Cannot open $gds_top.spf_$mode\n");
    @file = <SPF>;
  close SPF;

  open(SPF, "> $gds_top.spf_$mode") or die "[", color("red", color("reset"), "] Cannot open $gds_top.spf_$mode\n");
    foreach my $line(@file) {
      $line =~ s/\sLFUSE\s/ /g;
      print SPF $line;
  }
  close SPF;
}

if($change_device_format eq YES) {
  print"Post-process LPE netlist ...\n";
  open(SPF, "< $gds_top.spf_$mode") || die "[", color("red", color("reset"), "] Cannot open $gds_top.spf_$mode\n");
    @file = <SPF>;
  close SPF;

  open(SPF, "> $gds_top.spf_$mode") or die "[", color("red", color("reset"), "] Cannot open $gds_top.spf_$mode\n");
    foreach my $line(@file) {
    if($line =~ m/^\*\|I/) {
      $line =~ s/\/MM/\/XMM/g;
      $line =~ s/\/DD/\/XDD/g;
      $line =~ s/\/RR/\/XRR/g;
      $line =~ s/\/CC/\/XCC/g;
      $line =~ s/\.MM/\.XMM/g;
      $line =~ s/\.DD/\.XDD/g;
      $line =~ s/\.RR/\.XRR/g;
      $line =~ s/\.CC/\.XCC/g;
      print SPF $line;
    }
    else {
      $line =~ s/^XX(\S+)\/MM(\S+)/XX$1\/XMM$2/g;
      $line =~ s/^XX(\S+)\/DD(\S+)/XX$1\/XDD$2/g;
      $line =~ s/^XX(\S+)\/RR(\S+)/XX$1\/XRR$2/g;
      $line =~ s/^XX(\S+)\/CC(\S+)/XX$1\/XCC$2/g;
      $line =~ s/(\S+)\/MM(\S+):DRN/$1\/XMM$2:DRN/g;
      $line =~ s/(\S+)\/MM(\S+):GATE/$1\/XMM$2:GATE/g;
      $line =~ s/(\S+)\/MM(\S+):SRC/$1\/XMM$2:SRC/g;
      $line =~ s/(\S+)\/MM(\S+):BULK/$1\/XMM$2:BULK/g;
      $line =~ s/(\S+)\/DD(\S+):A/$1\/XDD$2:A/g;
      ##$line =~ s/(\S+)\/DD(\S+):B/$1\/XDD$2:B/g;
      $line =~ s/(\S+)\/DD(\S+):C/$1\/XDD$2:C/g;    ## 2023-08-03, pcao modify to fix DD bug
      $line =~ s/(\S+)\/RR(\S+):A/$1\/XRR$2:A/g;
      $line =~ s/(\S+)\/RR(\S+):B/$1\/XRR$2:B/g;
      $line =~ s/(\S+)\/CC(\S+):A/$1\/XCC$2:A/g;
      $line =~ s/(\S+)\/CC(\S+):B/$1\/XCC$2:B/g;
      $line =~ s/^XX(\S+)\.MM(\S+)/XX$1\.XMM$2/g;
      $line =~ s/^XX(\S+)\.DD(\S+)/XX$1\.XDD$2/g;
      $line =~ s/^XX(\S+)\.RR(\S+)/XX$1\.XRR$2/g;
      $line =~ s/^XX(\S+)\.CC(\S+)/XX$1\.XCC$2/g;
      $line =~ s/(\S+)\.MM(\S+):DRN/$1\.XMM$2:DRN/g;
      $line =~ s/(\S+)\.MM(\S+):GATE/$1\.XMM$2:GATE/g;
      $line =~ s/(\S+)\.MM(\S+):SRC/$1\.XMM$2:SRC/g;
      $line =~ s/(\S+)\.MM(\S+):BULK/$1\.XMM$2:BULK/g;
      $line =~ s/(\S+)\.DD(\S+):A/$1\.XDD$2:A/g;
      ##$line =~ s/(\S+)\.DD(\S+):B/$1\.XDD$2:B/g;
      $line =~ s/(\S+)\.DD(\S+):C/$1\.XDD$2:C/g;    ## 2023-08-03, pcao modify to fix DD bug
      $line =~ s/(\S+)\.RR(\S+):A/$1\.XRR$2:A/g;
      $line =~ s/(\S+)\.RR(\S+):B/$1\.XRR$2:B/g;
      $line =~ s/(\S+)\.CC(\S+):A/$1\.XCC$2:A/g;
      $line =~ s/(\S+)\.CC(\S+):B/$1\.XCC$2:B/g;
      $line =~ s/^XX/X/g;
      print SPF $line;
    }
    }
  close SPF;
}

if($ba_diode eq YES) {
  print"Generate new SPF netlist for BA_Diode flow ...\n";
  open(SPF, "< $gds_top.spf_$mode") || die "[", color("red", color("reset"), "] Cannot open $gds_top.spf_$mode\n");
    @file = <SPF>;
  close SPF;

  open(SPF, "> $gds_top.spf_$mode\_BA") or die "[", color("red", color("reset"), "] Cannot open $gds_top.spf_$mode\_BA\n");
    foreach my $line(@file) {
      $line =~ s/^\s*DXI_/XI_/g;
      print SPF $line;
  }
  close SPF;
}

if($Cap_Rep eq YES) {
  print "Generate Total Cap Report ...\n";
  my %net_cap;
  open(SPF, "< $gds_top.spf_$mode") || die "[", color("red", color("reset"), "] Cannot open $gds_top.spf_$mode\n");
    @file = <SPF>;
  close SPF;

  open(SPF, "> $gds_top.$mode\_cap.rep") or die "[", color("red", color("reset"), "] Cannot open $gds_top.$mode\_cap.rep\n");
    foreach my $line(@file) {
      if($line =~ /^\*\|NET\s+(\S+)\s+(\S+)PF/) {
        $net_cap{$1} = $2;
      }
    }

  foreach my $key ( sort { $net_cap{$b} <=> $net_cap{$a} } keys %net_cap ) {
    my $value = $net_cap{$key};
    print SPF "$key $value"."PF\n";
  }
  close SPF;
}

print"\n^v^ StarRC extraction complete ^v^\n\n";

##Check Skip Cells Warning
open(SKIP_CELL_WARNING, "< $gds_top.star_sum") or die "[", color("red", color("reset"), "] Cannot open $gds_top.star_sum\n");
  foreach $line(<SKIP_CELL_WARNING>) {
    if($line =~ m/WARNING\: SKIP_CELLS list member "(.*)" .* will be ignored/) {
      print "--> \"$1\" is not be skipped during StarRC extraction, Please check your SKIP_CELL setting!!\n";
    }
   }
  print "\n";
close SKIP_CELL_WARNING;

##sub scripts
## Wens print the missed options
sub check_config {
  my ($options, $optnames) = @_;
  my @tmpOption = @$options;
  my @tmpOptnames = @$optnames;
  my $errflag;
  for(my $i=0; $i<=$#tmpOption; $i++){
    if($tmpOption[$i] eq ""){
      $errflag = 1;
      if($missopt){
        $missopt .= ", $tmpOptnames[$i]";
      }else{
        $missopt = $tmpOptnames[$i];
      }
    }
  }
  if($errflag == 1){
    print "\nYour local lpe.config missing option -- $missopt !!\n\n";
    print "Please use central lpe.config -> /apps/imctf/cad/script/runlpe/lpe.config\n\n";
    exit();
  }

open(CONFIG_default,"</apps/imctf/cad/script/runlpe/lpe.config") || die "[", color("red", color("reset"), "] Cannot open lpe.config\n");
  while(<CONFIG_default>) {
    $virtual_connect_default = $1 if /^\s*VIRTUAL_CONNECT\s*=\s*(\S+)/i;
    $select_nets_default = $1 if /^\s*NETS\s*=\s*(.*)/i;
    $netlist_type_default = $1 if /^\s*PG_Ronly_NETS\s*=\s*(.*)/i;
    $netlist_instance_section_default = $1 if /^\s*NETLIST_INSTANCE_SECTION\s*=\s*(.*)/i;
    $net_type_default = $1 if /^\s*NET_TYPE\s*=\s*(\S+)/i;
    $cell_type_default = $1 if /^\s*CELL_TYPE\s*=\s*(\S+)/i;
    $power_extract_default = $1 if /^\s*POWER_EXTRACT\s*=\s*(\S+)/i;
    $power_nets_default = $1 if /^\s*POWER_NETS\s*=\s*(.*)/i;
    $Keep_Power_default = $1 if /^\s*Keep_Power\s*=\s*(.*)/i;
    $device_coordinate_default = $1 if /^\s*DEVICE_COORDINATE\s*=\s*(\S+)/i;
    $placement_info_default = $1 if /^\s*PLACEMENT_INFO_FILE\s*=\s*(\S+)/i;
    $reduction_default = $1 if /^\s*REDUCTION\s*=\s*(\S+)/i;
    $coupling_abs_threshold_default = $1 if /^\s*COUPLING_ABS_THRESHOLD\s*=\s*(\S+)/i;
    $coupling_rel_threshold_default = $1 if /^\s*COUPLING_REL_THRESHOLD\s*=\s*(\S+)/i;
    $floating_as_fill_default = $1 if /^\s*FLOATING_AS_FILL\s*=\s*(\S+)/i;
    $hierarchical_separator_default = $1 if /^\s*HIERARCHICAL_SEPARATOR\s*=\s*(\S+)/i;
    $netlist_nodename_netname_default = $1 if /^\s*NETLIST_NODENAME_NETNAME\s*=\s*(\S+)/i;
    $change_device_format_default = $1 if /^\s*CHANGE_DEVICE_FORMAT\s*=\s*(\S+)/i;
    $netlist_subckt_default = $1 if /^\s*NETLIST_SUBCKT\s*=\s*(\S+)/i;
    $r3d_default = $1 if /^\s*R3D\s*=\s*(\S+)/i;
    $lpe_lvs_default = $1 if /^\s*CHK_LPE_LVS\s*=\s*(\S+)/i;
    $Sub_Dio_default = $1 if /^\s*Sub_Dio\s*=\s*(\S+)/i;
    $spres_default = $1 if /^\s*SPRES\s*=\s*(\S+)/i;
    $ba_diode_default = $1 if /^\s*BA_Diode\s*=\s*(\S+)/i;
    $Core_Num_default = $1 if /^\s*Core_Num\s*=\s*(\S+)/i;
    $Cap_Rep_default = $1 if /^\s*Cap_Rep\s*=\s*(\S+)/i;
    $bulk_default = $1 if /^\s*BULK\s*=\s*(\S+)/i;
}
close CONFIG_default;
open(CONFIG_SETTING, ">lpe_config.setting") || die "[", color("red", color("reset"), "] Cannot open lpe_config.setting\n");
    print CONFIG_SETTING "Following options is unmatched to central default setting:\n\n";
    if($virtual_connect ne $virtual_connect_default) {print CONFIG_SETTING "VIRTUAL_CONNECT=> $virtual_connect vs $virtual_connect_default\n";}
    if($select_nets ne $select_nets_default) {print CONFIG_SETTING "NETS=> $select_nets vs $select_nets_default\n";}
    if($netlist_type ne $netlist_type_default) {print CONFIG_SETTING "PG_Ronly_NETS=> $netlist_type vs $netlist_type_default\n";}
    if($netlist_instance_section ne $netlist_instance_section_default) {print CONFIG_SETTING "NETLIST_INSTANCE_SECTION=> $netlist_instance_section vs $netlist_instance_section_default\n";}
    if($net_type ne $net_type_default) {print CONFIG_SETTING "NET_TYPE=> $net_type vs $net_type_default\n";}
    if($cell_type ne $cell_type_default) {print CONFIG_SETTING "CELL_TYPE=> $cell_type vs $cell_type_default\n";}
    if($power_extract ne $power_extract_default) {print CONFIG_SETTING "POWER_EXTRACT=> $power_extract vs $power_extract_default\n";}
    if($power_nets ne $power_nets_default) {print CONFIG_SETTING "POWER_NETS=> $power_nets vs $power_nets_default\n";}
    if($Keep_Power ne $Keep_Power_default) {print CONFIG_SETTING "Keep_Power=> $Keep_Power vs $Keep_Power_default\n";}
    if($device_coordinate ne $device_coordinate_default) {print CONFIG_SETTING "DEVICE_COORDINATE=> $device_coordinate vs $device_coordinate_default\n";}
    if($placement_info ne $placement_info_default) {print CONFIG_SETTING "PLACEMENT_INFO_FILE=> $placement_info vs $placement_info_default\n";}
    if($reduction ne $reduction_default) {print CONFIG_SETTING "REDUCTION=> $reduction vs $reduction_default\n";}
    if($coupling_abs_threshold ne $coupling_abs_threshold_default) {print CONFIG_SETTING "COUPLING_ABS_THRESHOLD=> $coupling_abs_threshold vs $coupling_abs_threshold_default\n";}
    if($coupling_rel_threshold ne $coupling_rel_threshold_default) {print CONFIG_SETTING "COUPLING_REL_THRESHOLD=> $coupling_rel_threshold vs $coupling_rel_threshold_default\n";}
    if($floating_as_fill ne $floating_as_fill_default) {print CONFIG_SETTING "FLOATING_AS_FILL=> $floating_as_fill vs $floating_as_fill_default\n";}
    if($hierarchical_separator ne $hierarchical_separator_default) {print CONFIG_SETTING "HIERARCHICAL_SEPARATOR=> $hierarchical_separator vs $hierarchical_separator_default\n";}
    if($netlist_nodename_netname ne $netlist_nodename_netname_default) {print CONFIG_SETTING "NETLIST_NODENAME_NETNAME=> $netlist_nodename_netname vs $netlist_nodename_netname_default\n";}
    if($change_device_format ne $change_device_format_default) {print CONFIG_SETTING "CHANGE_DEVICE_FORMAT=> $change_device_format vs $change_device_format_default\n";}
    if($netlist_subckt ne $netlist_subckt_default) {print CONFIG_SETTING "NETLIST_SUBCKT=> $netlist_subckt vs $netlist_subckt_default\n";}
    if($r3d ne $r3d_default) {print CONFIG_SETTING "R3D=> $r3d vs $r3d_default\n";}
    if($lpe_lvs ne $lpe_lvs_default) {print CONFIG_SETTING "CHK_LPE_LVS=> $lpe_lvs vs $lpe_lvs_default\n";}
    if($Sub_Dio ne $Sub_Dio_default) {print CONFIG_SETTING "Sub_Dio=> $Sub_Dio vs $Sub_Dio_default\n";}
    if($spres ne $spres_default) {print CONFIG_SETTING "SPRES=> $spres vs $spres_default\n";}
    if($ba_diode ne $ba_diode_default) {print CONFIG_SETTING "BA_Diode=> $ba_diode vs $ba_diode_default\n";}
    if($Core_Num ne $Core_Num_default) {print CONFIG_SETTING "Core_Num=> $Core_Num vs $Core_Num_default\n";}
    if($Cap_Rep ne $Cap_Rep_default) {print CONFIG_SETTING "Cap_Rep=> $Cap_Rep vs $Cap_Rep_default\n";}
    if($bulk ne $bulk_default) {print CONFIG_SETTING "BULK=> $bulk vs $bulk_default\n";}
close CONFIG_SETTING;
}

sub help {
print qq~
***********************
** runlpe for StarRC **
***********************

=> Usage:
    % runlpe -config lpe.config

    % script   -> /apps/imctf/cad/script/runlpe/runlpe
    % template -> /apps/imctf/cad/script/runlpe/lpe.config

-------------------------
-> Version    :2.0
-> Author     :Kobe Weng
-------------------------
~;
 exit();
}
