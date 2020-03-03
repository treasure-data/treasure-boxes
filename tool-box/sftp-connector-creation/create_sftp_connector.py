import pysftp
from stat import S_ISDIR, S_ISREG
from config_sftp import database_name, remotedir, \
    sftp_folder_name, is_data_load_initially, \
    cron, seed_file, sftpHostname, \
    sftpUsername, sftpPassword
import yaml
import subprocess
import os
import re

def file_cleanup(directory):
    """
    Clean up the yml files ending with .yml.*
    :param directory:
    :return: Nothing
    """
    try:
        pattern = r'\.yml\.[0-9]$'
        for filename in os.listdir(directory):
            if re.search(pattern, filename):
                os.remove(os.path.join(directory, filename))
                # print('File removed: ', filename)
            else:
                continue
    except Exception as e:
        print('Something went wrong in file_cleanup', str(e))


def _sftp_helper(sftp, files):
    """
    Create the List of files available on sftp
    :param sftp:
    :param files:
    :return: Nothing
    """
    stats = sftp.listdir_attr('.')
    files[sftp.getcwd()] = [attr.filename for attr in stats if S_ISREG(attr.st_mode)]

    for attr in stats:
        if S_ISDIR(attr.st_mode):  # If the file is a directory, recurse it
            sftp.chdir(attr.filename)
            _sftp_helper(sftp, files)
            sftp.chdir('..')


def filelist_recursive(sftp):
    """
    Returning the list of files
    :param sftp:
    :return:
    """
    files = {}
    _sftp_helper(sftp, files)
    return files


def create_seed_yml(seed_file, path_prefix, db_name, table_name):
    """
    Create the seed file
    :param seed_file:
    :param path_prefix:
    :param db_name:
    :param table_name:
    :return: seed file name
    """
    with open(seed_file, 'r') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        yml_file = yaml.load(file, Loader=yaml.FullLoader)
        # print(yml_file)
        yml_file['in']['path_prefix'] = path_prefix
        yml_file['out']['database'] = db_name
        yml_file['out']['table'] = table_name

    # actual_seed_filename = (path_prefix.split('/')[-1].split('.')[0]).replace(' ', '_')
    file_new = directory + '/seed_' + table_name + '.yml'
    file_new = r"{}".format(file_new)
    with open(file_new, 'w') as f:
        yaml.dump(yml_file, f, default_flow_style=False)
    print(f'file {file_new} is created successfully.')
    return file_new


def convert_all_cols_to_string(guessed_file):
    """
    Convert all non string columns to string
    :param guessed_file:
    :return: updated 'load1_' File name
    """
    new_column_list = []
    with open(guessed_file, 'r') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        yml_file = yaml.load(file, Loader=yaml.FullLoader)
        # print(yml_file)
        col_list = yml_file.get('in').get('parser').get('columns')
        # print(col_list)
        for elements in col_list:
            # print(elements)
            if elements.get('type') != 'string':
                # if elements.get('format'):
                #     del elements['format']
                elements['type'] = 'string'
            # print(elements)
            new_column_list.append(elements)
        # print(new_column_list)
        yml_file['in']['parser']['columns'] = new_column_list
        # print(yml_file)

    file_new = guessed_file.replace('load_', 'load1_')
    file_new = r"{}".format(file_new)
    with open(file_new, 'w') as f:
        yaml.dump(yml_file, f, default_flow_style=False)
    print(f'file {file_new} is created successfully.')
    return file_new


def run_td_command(cmd, cmd_type):
    """
    Run the TD command provided and capture the error if found any
    :param cmd:
    :param cmd_type:
    :return: Nothing
    """
    print(f'Running command: {cmd}')
    try:
        error_msg_local = {}
        results = subprocess.run(
            cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        returncode = results.returncode
        print('returncode: ', returncode)
        if returncode != 0:
            error_msg_local[cmd_type] = {'failed_command': cmd, 'returncode': returncode,
                                         'error_msg': results.stderr + results.stdout}
            # print(error_msg_local)
            # import multiple errors as list for same cmd_type if any
            try:
                for key, val in error_msg_local.items():
                    error_msg[key].append(val)
            except KeyError:
                error_msg[key] = [val]
        else:
            pass
            # print(f'Command "{cmd}" ran successfully')
    except subprocess.CalledProcessError as e:
        print(str(e))
    except Exception as e:
        print('Something Went Wrong...', str(e))


# Code Starts From Here

# TD Connector Commands
td_guess_cmd = 'td connector:guess {seed_file} -o {guessed_file}'
td_cc_cmd = 'td connector:create {name} {cron} {database} {table} {config}'
td_create_table_cmd = 'td table:create {database} {table}'

error_msg = {}

if not os.path.exists('yml_files'):
    os.mkdir('yml_files')

cwd = os.getcwd()
directory = os.path.join(cwd, 'yml_files')

# File cleanup
file_cleanup(directory)


# PLACE HOLDER FOR ADDING CODE TO HANDLE THE ENCRYTION STUFF
def main(seed_file):
    try:
        with pysftp.Connection(host=sftpHostname, username=sftpUsername, password=sftpPassword) as sftp:
            print("Connection succesfully established ... ")

            # Switch to a remote directory
            remotedir1 = remotedir + '/' + sftp_folder_name
            sftp.cwd(remotedir1)

            # Obtain structure of the remote directory '/var/ftp/Adobe_Analytics'
            results = filelist_recursive(sftp)
            # print(results)
            for folder, file in results.items():
                print('#' * 80)
                print('Below Folder is being processed...\n', folder, file)
                if folder and file:
                    for f in file:
                        print('*' * 80)
                        # f = f.replace(remotedir, '')
                        file_name_without_ext = f.split('.')[0]
                        # print(file_name_without_ext)
                        abs_path = folder.replace(remotedir, '') + '/' + f
                        abs_path = abs_path.split('.')[0]
                        parent_folder = abs_path.split('/')[1]  # /CRM/file.csv, CRM is extracted.
                        file_name_without_ext = parent_folder + '_' + file_name_without_ext
                        file_name_without_ext = file_name_without_ext.replace(' ', '_').lower()
                        # print(abs_path)
                        # PLACE HOLDER FOR CREATING THE CONNECTORS

                        seed_file = create_seed_yml(seed_file=seed_file,
                                                    path_prefix=abs_path,
                                                    db_name=database_name,
                                                    table_name=file_name_without_ext
                                                    )
                        guessed_file = seed_file.replace('seed', 'load')
                        td_guess_cmd_1 = td_guess_cmd.format(seed_file=seed_file,
                                                             guessed_file=guessed_file
                                                             )
                        # print(td_guess_cmd_1)

                        # run the guess command
                        run_td_command(td_guess_cmd_1, file_name_without_ext)

                        # convert all column data type to sting
                        updated_guessed_filename = convert_all_cols_to_string(guessed_file)

                        # Creating the table which is used in connector
                        create_tbl_cmd = td_create_table_cmd.format(database=database_name,
                                                                    table=file_name_without_ext
                                                                    )
                        # print('create_tbl_cmd: ', create_tbl_cmd)
                        # run the create_tbl_cmd command
                        run_td_command(create_tbl_cmd, file_name_without_ext)

                        # Call function to create the connector
                        connector_name = 'ap_src' + abs_path.replace('/', '_').replace(' ', '_').lower()
                        print('connector_name: ', connector_name)
                        td_cc_cmd_1 = td_cc_cmd.format(name=connector_name,
                                                       cron=cron,
                                                       database=database_name,
                                                       table=file_name_without_ext,
                                                       config=updated_guessed_filename
                                                       )
                        # print(td_cc_cmd_1)

                        # run the create cconnector command
                        run_td_command(td_cc_cmd_1, file_name_without_ext)
                        # print(f'Connector {connector_name} created successfully...')

                        if is_data_load_initially:
                            run_connector_command = f'td connector:run {connector_name}'
                            # run the create_tbl_cmd command
                            run_td_command(run_connector_command, file_name_without_ext)
                            print(f'Table {file_name_without_ext} is loaded successfully.')

                else:
                    print('This ', folder, 'is empty')
    except Exception as e:
        print('Something Went Wrong... Please check.', str(e))
        raise

    print('#' * 80, '\n')
    # File cleanup
    file_cleanup(directory)

    if error_msg:
        print('Below are list of commands which fails...')
        print(error_msg)
    else:
        print('Yay!!! Connectors created successfully... Please check UI.')

if __name__ == '__main__':
    # call main method
    print('In Main')
    main(seed_file)
