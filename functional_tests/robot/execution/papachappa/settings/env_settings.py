import os


remote_lib_host = "192.168.108.26"        # where sip and sbc libraries reside
remote_target_host = "192.168.108.26"      # testing host or device
remote_lib_port = "8002"
itc_host_ip = "192.168.7.142"


sipp_A_remote_lib_port = "8050"
sipp_B_remote_lib_port = "8051"
sipp_C_remote_lib_port = "8052"


CRS_REMOTE_PATH = '/usr/protei/Protei-CRS/Voice'
CRS_BE_REMOTE_PATH = '/usr/protei/Protei-CRS/BE'
CRS_META_REMOTE_PATH = '/usr/protei/Protei-CRS/Meta'
CRS_STORAGE_REMOTE_PATH = '/usr/protei/Protei-CRS-Storage'
CRS_STORAGE_REMOTE_PATH_ANOTHER = '/var/fs4'
CRS_STORAGE_REMOTE_PATH_YET_ANOTHER = '/var/fs5'

CRS_MKD_REMOTE_PATH = "/usr/protei/Protei-MKD/MKD"
CRS_MCU_REMOTE_PATH = "/usr/protei/Protei-MKD/MCU"
MVSIP_REMOTE_PATH = "/usr/protei/Protei-MV.SIP"
MTS_REMOTE_PATH = "/var/mts/bin"
MTS_REMOTE_TEST_PATH = "/var/mts/testsuites"
MTS_REMOTE_LOG_PATH = "/var/mts/logs"
REPLICA_AGENT_PATH = "/usr/protei/Protei-CRS/Replica-Agent"
REPLICA_CLIENT_PATH = "/usr/protei/Protei-CRS/Replica-Client"
NEW_CRS_STORAGE = '/usr/protei/Protei-CRS/Voice/storage'
BACK_CRS_STORAGE = '/var/protei/Protei-CRS-Storage'

CRS_LOGS_DIR = '/usr/protei/Protei-CRS/Voice/logs'
META_LOGS_DIR = '/usr/protei/Protei-CRS-Storage/meta/local'
SUPPORT_HOME_DIR = '/home/support/'
ROOT_HOME_DIR = '/root/'

RecordingList_File = '/usr/protei/Protei-CRS-Storage/voice/local/RecordingList.txt'

REMOTE_LIB_PATH = "%s/robot" % CRS_REMOTE_PATH

ROBOTDIR = os.path.abspath('./../../..')
#SCENARIO_PATH = "/var/protei/robot"
SCENARIO_PATH = "/usr/protei/Protei-CRS/Voice/robot_logs"
EXECUTION_LIB_PATH = "%s/execution/lib/" % ROBOTDIR

COMMON_SETTINGS_FILE = "%s/implementation/resources/common_settings.txt" % ROBOTDIR
