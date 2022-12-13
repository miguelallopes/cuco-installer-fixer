import ctypes ,wmi, httpx
from sys import argv, executable
import os,  shutil
from time import sleep


# ------------------------------------------------------------------------------------------------
#
#                                Get administrator permission
#
# ------------------------------------------------------------------------------------------------

class LocationCUCO:
    SYS = "C:\\Windows\\System32\\"
    EDF2 = "C:\\Recovery\\OEM\\Scripts\\"
    JPIK = "C:\\Recovery\\OEM\\"


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def identify_manufacturer_and_model():
    wmi_conn = wmi.WMI()
    wmi_conn_cs = wmi_conn.Win32_ComputerSystem()[0]

    manufacturer = wmi_conn_cs.Manufacturer
    model = wmi_conn_cs.Model

    return {"manufacturer": manufacturer, "model": model}

def reinstall_cuco_service(system: LocationCUCO):
    print("Success")

     # Step 3 - Remove from quarantine and add exclusions to AV
     
    print("[STEP 3] Remove from quarantine and add exclusions to Windows Defender AV... ")
    # os.system('"C:\Program Files\Windows Defender\MpCmdRun.exe" -restore -filepath "{system}agent.exe"')
    # os.system('"C:\Program Files\Windows Defender\MpCmdRun.exe" -restore -filepath "%~dp0agent.exe"')

    os.system(f'powershell -command "Set-ExecutionPolicy -ExecutionPolicy Unrestricted"')
    os.system(f'powershell -Command Add-MpPreference -ExclusionProcess "{system}agent.exe"')
    os.system(f'powershell -Command Add-MpPreference -ExclusionProcess "%~dp0agent.exe"')
    print("         Successfuly applied AV configurations")

    
    print("[STEP 4] Updating Windows Defender AV signatures... ")
    
    os.system(f'"C:\Program Files\Windows Defender\MpCmdRun.exe" -removedefinitions -dynamicsignatures')
    os.system(f'"C:\Program Files\Windows Defender\MpCmdRun.exe" -SignatureUpdate')
    print("         Successfuly updated AV signatures")

    # Step 1 - Download agent
    print("[STEP 5] Downloading CucoService from inforlandia servers... ", end="")
    success = False
    while not success:
        try:
            response = httpx.get(
                "https://cuco.inforlandia.pt/uagent/agent.exe"
            )
            # raise HTTPError
            response.raise_for_status()
            with open("agent.new", "wb") as agent:
                agent.write(response.content)
                
        except httpx.HTTPError as err:
            
            print("\n         Download failed, check your network connection or firewall. Retrying in 5 seconds")
            sleep(5)
        else:
            print('\n         Download successful, file saved in actual directory as "agent.new"')
            success = True
    
    
    
    print("[STEP 6] Cuco Agent is already installed? ", end="")
    if not os.path.isfile(system + "agent.exe"):
        # CUCOService needs to be installed from source
        print("False")
        
        # Step 2 - Move file to system
        print('[STEP 7] Copying "agent.exe" to system folder... ', end="")
        if not os.path.exists(system):
            os.mkdir(system)
        shutil.copy("agent.new", system + "agent.exe")
        print("Success")

        # Step 3 - Evoke installation
        print('[STEP 8] Installing Cuco Agent and Service... ', end="")
        os.system(system + "agent.exe install")
        print("Success")
        
        print('[STEP 9] Starting Cuco Agent and Service... ', end="")
        os.system(system + "agent.exe start")
        print("Success")


        print('[STEP 10] Removing old Cuco configuration if exists... ', end="")
        try:
            os.remove(system + "agent.cfg")
        except OSError:
            print("Not found")
        else:
            print("Found")
        
        # Step 4 - Run CucoService
        print('[STEP 11] Run Cuco Agent and Service... ', end="")
        os.system(system + "agent.exe run")
        print("Success\n\n")

        input("Cuco Service and Agent is successfuly installed! Press ENTER to continue...")



    else:
        print("True")

       

        # Step 5 - Stop and Uninstall CucoService
        
        print('[STEP 7] Stopping Cuco Agent and Service... ', end="")
        os.system(system + "agent.exe stop")
        print("Success")

        print('[STEP 8] Removing Cuco Agent and Service... ', end="")
        os.system(system + "agent.exe remove")
        os.remove(system + "agent.exe")
        print("Success")

        # Step 6 - Move file to system
        print('[STEP 9] Copying updated "agent.exe" to system folder... ', end="")
        shutil.copy("agent.new", system + "agent.exe")
        print("Success")

        # Step 7 - Evoke installation
        
        print('[STEP 10] Installing Cuco Agent and Service... ', end="")
        os.system(system + "agent.exe install")
        print("Success")
        print('[STEP 11] Starting Cuco Agent and Service... ', end="")
        os.system(system + "agent.exe start")
        print("Success")

        # Step 8 - Remove old configuration
        print('[STEP 12] Removing old Cuco configuration if exists... ', end="")
        try:
            os.remove(system + "agent.cfg")
        except OSError:
            print("Not found")
        else:
            print("Found")
        # Step 9 - Run CucoService
        print('[STEP 13] Run Cuco Agent and Service... ', end="")
        os.system(system + "agent.exe run")
        print("Success\n\n")

        input("Cuco Service and Agent is successfuly reinstalled! Press ENTER to continue...")

    try:
        os.remove("agent.new")
    except OSError:
        pass
if __name__ == "__main__":

    print("++++++++++++++++++++++++++++++++++++++")
    print("+                                    +")
    print("+       Cuco Installer & Fixer       +")
    print("+     Release 0.1.0 by PWRScript     +")
    print("+                                    +")
    print("++++++++++++++++++++++++++++++++++++++")
    sleep(1)

    os.system('title "Cuco Installer & Fixer"')

    print("[STEP 1] Looking for administrator priviledges... ", end="")
    sleep(0.5)
    if not is_admin():
        print("Failed\n         Restarting installer with appropriate permissions")
        sleep(2)
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, " ".join(argv), None, 1)
    else:
        print("Success")

        print("[STEP 2] Verifying if this computer can install CucoService... ", end="")
        sleep(0.5)
        computer = identify_manufacturer_and_model()

        if computer["model"] in ["WH1-140P", "YK1-140C", "PT1-140C", "PT1-140CI", "GW1-W148"]:
            reinstall_cuco_service(LocationCUCO.SYS)

        elif computer["model"] in ["GW1-W149", "HN1-K14C", "YK1-K14C", "WH1-K14C"]:
            reinstall_cuco_service(LocationCUCO.EDF2)

        elif os.path.isfile("C:\Windows\System32\agent.exe"):
            reinstall_cuco_service(LocationCUCO.SYS)

        elif computer["manufacturer"] in ["JP.ik", "MEDION", "LNV"]:
            reinstall_cuco_service(LocationCUCO.JPIK)

        elif os.path.isfile("C:\Recovery\OEM\agent.exe"):
            reinstall_cuco_service(LocationCUCO.JPIK)

        else:
            print(f"Failed\n         {computer['manufacturer']} {computer['model']} is not compatible, installer will exit\n\nExiting in 5 seconds")
            sleep(5)
