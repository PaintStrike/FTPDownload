from ftplib import FTP
import os

def connect_ftp(server, username, password):
    ftp = FTP(server)
    ftp.login(username, password)
    return ftp

def download_file(ftp, remote_path, local_path):
    with open(local_path, 'wb') as local_file:
        ftp.retrbinary(f'RETR {remote_path}', local_file.write)

def download_folder(ftp, remote_folder, local_folder):
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)
    
    original_cwd = ftp.pwd()  # Store the original working directory
    ftp.cwd(remote_folder)
    
    for name, attrs in ftp.mlsd():
        local_path = os.path.join(local_folder, name)
        
        if attrs['type'] == 'file':
            download_file(ftp, name, local_path)
        elif attrs['type'] == 'dir':
            new_remote = f"{remote_folder}/{name}"
            new_local = os.path.join(local_folder, name)
            download_folder(ftp, new_remote, new_local)

    ftp.cwd(original_cwd)  # Change back to the original directory

if __name__ == "__main__":
    server = 'ftp.server.com'
    username = 'user'
    password = 'password'
    
    target_folder = input("Enter the folder name to download: ")  # Get folder name from user
    remote_target_folder = f"licenses/{target_folder}"
    
    local_target_folder = target_folder  # Local folder name will be the same as the target folder
    ftp = connect_ftp(server, username, password)

    download_folder(ftp, remote_target_folder, local_target_folder)
    ftp.quit()


#This script logs in at the ftp and goes into the folder "licenses" (as the line 38 specifies) and downloads the folder/file (asked in line 37) saving it at the same directory as this file.
