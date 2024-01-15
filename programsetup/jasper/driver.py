import sys
import json
import subprocess
import os
import shutil
import git

from git import Repo

KEY_CATEGORY = "category"
KEY_DONOR = "donor"
KEY_TARGET = "target"
KEY_BUG_NAME = "bug_name"
KEY_POC_PATH = "poc"
KEY_CVE_ID = "cve"
KEY_TEST_ID = "id"

ARG_DATA_PATH = "--data-dir="
ARG_TOOL_PATH = "--tool-path="
ARG_TOOL_NAME = "--tool-name="
ARG_TOOL_PARAMS = "--tool-param="
ARG_DEBUG_MODE = "--debug"
ARG_SKIP_SETUP = "--skip-setup"
ARG_ONLY_SETUP = "--only-setup"
ARG_ANALYSE_MODE = "--analyse"
ARG_UPDATE_TEST = "--update-test"
ARG_START_ID = "--start-id="
ARG_END_ID = "--end-id="
ARG_BUG_ID = "--bug-id="
ARG_BUG_ID_LIST = "--bug-id-list="
ARG_DATA_SET = "--data="

CONF_DATA_PATH = "/data"
CONF_TOOL_PATH = "/FixMorph"
CONF_TOOL_PARAMS = ""
CONF_TOOL_NAME = "python3.7 Sosreverter.py"
CONF_DEBUG = False
CONF_SKIP_SETUP = False
CONF_ONLY_SETUP = False
CONF_START_ID = None
CONF_END_ID = None
CONF_BUG_ID = None
CONF_BUG_ID_LIST = None
CONF_UPDATE_TEST = False
CONF_ANALYSIS_MODE = False
CONF_DATA_SET = ""

# FILE_META_DATA = "issta21.json"
FILE_ERROR_LOG = "error-log"


DIR_MAIN = os.getcwd()
DIR_LOGS = DIR_MAIN + "/logs"
DIR_SCRIPT = DIR_MAIN + "/scripts"
DIR_CONF = DIR_MAIN + "/configuration"
DIR_EXPERIMENT = ""

REPO_PROGRAM = "jasper"
REPO_URL = "https://github.com/jasper-software/jasper.git"
REPO_PATH = "/" + REPO_PROGRAM

COUNT_SUCCESS = 0
COUNT_IDENTICAL = 0
COUNT_BUILD_FAILED = 0
COUNT_VERIFY_FAILED = 0
COUNT_TRANSFORM_FAILED = 0
COUNT_EXPERIMENT = 0
COUNT_RUNTIME_ERRORS = 0
COUNT_FAILURES = 0

list_success = list()
list_build_failed = list()
list_verify_failed = list()
list_other_failed = list()

def copy_file(src_file, dst_file):
    if os.path.isfile(src_file):
        shutil.copyfile(src_file.strip(), dst_file.strip())

def create_directories():
    if not os.path.isdir(DIR_LOGS):
        os.makedirs(DIR_LOGS)

def read_arg(arg_list):
    global CONF_DATA_PATH, CONF_TOOL_NAME, CONF_TOOL_PARAMS, CONF_DATA_SET
    global CONF_TOOL_PATH, CONF_DEBUG, CONF_SKIP_SETUP, CONF_ONLY_SETUP, CONF_BUG_ID_LIST
    global CONF_BUG_ID, CONF_START_ID, CONF_END_ID, CONF_UPDATE_TEST, CONF_ANALYSIS_MODE
    print("[DRIVER] Reading configuration values")
    if len(arg_list) > 0:
        for arg in arg_list:
            print(arg)
            if ARG_DATA_PATH in arg:
                CONF_DATA_PATH = str(arg).replace(ARG_DATA_PATH, "")
            elif ARG_TOOL_NAME in arg:
                CONF_TOOL_NAME = str(arg).replace(ARG_TOOL_NAME, "")
            elif ARG_TOOL_PATH in arg:
                CONF_TOOL_PATH = str(arg).replace(ARG_TOOL_PATH, "")
            elif ARG_TOOL_PARAMS in arg:
                CONF_TOOL_PARAMS = str(arg).replace(ARG_TOOL_PARAMS, "")
            elif ARG_DEBUG_MODE in arg:
                CONF_DEBUG = True
            elif ARG_SKIP_SETUP in arg:
                CONF_SKIP_SETUP = True
            elif ARG_ONLY_SETUP in arg:
                CONF_ONLY_SETUP = True
            elif ARG_ANALYSE_MODE in arg:
                CONF_ANALYSIS_MODE = True
            elif ARG_BUG_ID_LIST in arg:
                CONF_BUG_ID_LIST = arg.replace(ARG_BUG_ID_LIST, "").split(",")
            elif ARG_UPDATE_TEST in arg:
                CONF_UPDATE_TEST = True
            elif ARG_DATA_SET in arg:
                CONF_DATA_SET = arg.replace(ARG_DATA_SET, "")
            elif ARG_START_ID in arg:
                CONF_START_ID = int(str(arg).replace(ARG_START_ID, ""))
            elif ARG_END_ID in arg:
                CONF_END_ID = int(str(arg).replace(ARG_END_ID, ""))
            elif ARG_BUG_ID in arg:
                CONF_BUG_ID = int(str(arg).replace(ARG_BUG_ID, ""))
            else:
                print("Usage: python driver [OPTIONS] ")
                print("Options are:")
                print("\t" + ARG_DATA_PATH + "\t| " + "directory for experiments")
                print("\t" + ARG_TOOL_NAME + "\t| " + "name of the tool")
                print("\t" + ARG_TOOL_PATH + "\t| " + "path of the tool")
                print("\t" + ARG_TOOL_PARAMS + "\t| " + "parameters for the tool")
                print("\t" + ARG_DEBUG_MODE + "\t| " + "enable debug mode")
                exit()

def clone_repo():
    global REPO_URL
    if not os.path.isdir(REPO_PATH):
        print("[DRIVER] Cloning remote repository\n")
        git.Repo.clone_from(REPO_URL, REPO_PATH)

def load_experiment():
    global experiment_list, CONF_DATA_SET
    print("[DRIVER] Loading experiment data\n")
    if not os.path.isfile(CONF_DATA_SET):
        exit("data-set not found")
    with open(CONF_DATA_SET, 'r') as in_file:
        json_data = json.load(in_file)
        # print(json_data)
        experiment_list = json_data

def get_parent_commit(base_dir_path_pa):
    repo = Repo(base_dir_path_pa)
    patch_commit_a = repo.head.commit
    parent_commit_a = patch_commit_a.parents
    print(parent_commit_a)
    print("patch_commit_a:" + str(patch_commit_a))
    print("parent_commit_a:" + str(parent_commit_a[0]))
    
    return str(parent_commit_a[0])

    # diff_list = parent_commit.diff(patch_commit)
    

def setup_each(base_dir_path, bug_id, commit_id_list):
    global FILE_ERROR_LOG, CONF_DATA_PATH, CONF_UPDATE_TEST
    print("\t[INFO] creating directories for experiment")
    postfix_list = ['a', 'b', 'c','e']
    bug_dir = base_dir_path + "/" + str(bug_id)
    fix_commit,fix_parent, target_commit = commit_id_list

    if not os.path.isdir(bug_dir) or CONF_UPDATE_TEST:
            os.makedirs(bug_dir)

    
    for i in range(0,4):
        dir_path = bug_dir+ "/p"+postfix_list[i]
        if not os.path.isdir(dir_path):
            shutil.copytree(REPO_PATH, dir_path)
        
    dir_path_a = bug_dir+ "/p"+postfix_list[0]
    repo_a = git.Repo(dir_path_a)
    repo_a.git.reset("--hard")
    repo_a.git.checkout(fix_commit)
    
    fix_parent = get_parent_commit(dir_path_a)

    dir_path_b = bug_dir+ "/p"+postfix_list[1]
    repo_b = git.Repo(dir_path_b)
    repo_b.git.reset("--hard")
    repo_b.git.checkout(fix_parent)
        # repo = git.Repo(dir_path)
        # repo.git.reset("--hard")
        # repo.git.checkout(commit_id_list[i])

    dir_path_c = bug_dir+ "/p"+postfix_list[2]
    repo_c = git.Repo(dir_path_c)
    repo_c.git.reset("--hard")
    repo_c.git.checkout(target_commit)
    
    if not CONF_ANALYSIS_MODE:
        if os.path.isdir(bug_dir + "/pc-patch"):
            shutil.rmtree(bug_dir + "/pc-patch")

    # print(fix_commit,fix_parent, target_commit)
    return fix_commit,fix_parent, target_commit

def write_conf_file(base_dir_path, object_a, object_c, bug_id, commit_list):
    print("\t[INFO] creating configuration")
    conf_file_name = "reverter.conf"
    dir_path = base_dir_path + "/" + str(bug_id)
    conf_file_path = dir_path + "/" + conf_file_name
    if os.path.isfile(conf_file_path):
        os.remove(conf_file_path)
    
    fix_parent, fix_commit, target_commit= commit_list
    # print(conf_file_path)
    with open(conf_file_path, 'w') as conf_file:
        content = "path_a:" + dir_path + "/pa\n"
        content += "path_b:" + dir_path + "/pb\n"
        content += "path_c:" + dir_path + "/pc\n"
        content += "path_e:" + dir_path + "/pe\n"
        content += "tag_id:" + str(bug_id) + "\n"
        content += "commit_a:" + fix_commit + "\n"
        content += "commit_b:" + fix_parent + "\n"
        content += "commit_c:" + target_commit + "\n"
        # content += "commit_e:" + target_fix_commit + "\n"
        # content += "config_command_a:make allyesconfig \n"
        # content += "config_command_c:make allyesconfig \n"
        content += "backport:true\n"
        content += "linux-kernel::true\n"
        if object_a is None:
            content += "build_command_a:skip\n"
            content += "build_command_c:skip\n"
        else:
            content += "build_command_a:make " + object_a + "\n"
            if object_c is None:
                content += "build_command_c:make " + object_a + "\n"
            else:
                content += "build_command_c:make " + object_c + "\n"
        content += "version-control:git\n"
        conf_file.write(content)
    return conf_file_path

def execute_command(command):
    if CONF_DEBUG:
        print("\t[COMMAND]" + command)
    process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (output, error) = process.communicate()
    return str(process.returncode)

def evaluate(conf_path, bug_id):
    global CONF_TOOL_PARAMS, CONF_TOOL_PATH, CONF_TOOL_NAME, DIR_LOGS, COUNT_SUCCESS, CONF_DATA_SET
    print("\t[INFO] running evaluation")
    tool_command = "{ cd " + CONF_TOOL_PATH + ";" + CONF_TOOL_NAME + " --conf=" + conf_path + " "+ CONF_TOOL_PARAMS + ";} 2> " + FILE_ERROR_LOG
    print(tool_command)
    ret_code = execute_command(tool_command)
    exp_dir = DIR_MAIN + "/" + str(bug_id)
    print(exp_dir)
    if not os.path.isdir(exp_dir):
        os.makedirs(exp_dir)
    if os.path.isdir(exp_dir + "/output"):
        shutil.rmtree(exp_dir + "/output")

    DIR_PREFIX = "/FixMorph/logs/" + REPO_PROGRAM + "-"
    if CONF_DATA_SET == "cve-data.json":
        DIR_PREFIX = "/FixMorph/logs/" +REPO_PROGRAM + "-cve-"
    
    print(DIR_PREFIX + str(bug_id))
    print(exp_dir + "/output")
    shutil.copytree(DIR_PREFIX + str(bug_id), exp_dir + "/output")
    copy_file(DIR_PREFIX + str(bug_id) + "/log-latest", exp_dir + "/log-latest")
    copy_file(DIR_PREFIX + str(bug_id) + "/log-make", exp_dir + "/log-make")
    copy_file(DIR_PREFIX + str(bug_id) + "/log-error", exp_dir + "/log-error")
    copy_file(DIR_PREFIX + str(bug_id) + "/log-command", exp_dir + "/log-command")

    return ret_code

def check_word_exist(file_path, keyword):
    with open(file_path, "r") as log_file:
        content = log_file.readlines()
        content_str = ''.join(content)
        if keyword in content_str:
            return True
    return False

def analyse_result(bug_id, log_file_path):
    global COUNT_SUCCESS, COUNT_FAILURES, COUNT_TRANSFORM_FAILED
    global COUNT_VERIFY_FAILED, COUNT_BUILD_FAILED, COUNT_RUNTIME_ERRORS

    is_build_failed = check_word_exist(log_file_path, "BUILD FAILED")
    is_verify = check_word_exist(log_file_path, "verifying compilation")
    is_success = check_word_exist(log_file_path, "FixMorph finished successfully")
    is_failed = check_word_exist(log_file_path, "exited with an error")
    is_runtime_error = not check_word_exist(log_file_path, "FAILED") and is_failed
    is_transform_failure = check_word_exist(log_file_path, "transformation FAILED")

    if is_success:
        COUNT_SUCCESS = COUNT_SUCCESS + 1
        list_success.append(bug_id)
    elif is_build_failed and is_verify:
        COUNT_VERIFY_FAILED = COUNT_VERIFY_FAILED + 1
        list_verify_failed.append(bug_id)
    elif is_build_failed and not is_verify:
        COUNT_BUILD_FAILED = COUNT_BUILD_FAILED + 1
        list_build_failed.append(bug_id)
    elif is_failed and not is_runtime_error:
        COUNT_FAILURES = COUNT_FAILURES + 1
    elif is_failed and is_runtime_error:
        COUNT_RUNTIME_ERRORS = COUNT_RUNTIME_ERRORS + 1
    elif is_transform_failure:
        COUNT_TRANSFORM_FAILED = COUNT_TRANSFORM_FAILED + 1
    else:
        list_other_failed.append(bug_id)

def write_as_json(data_list, output_file_path):
    content = json.dumps(data_list)
    with open(output_file_path, 'w') as out_file:
        out_file.writelines(content)

def run(arg_list):
    global experiment_list, DIR_MAIN, CONF_DATA_PATH, CONF_TOOL_PARAMS
    global DIR_EXPERIMENT, COUNT_IDENTICAL, COUNT_EXPERIMENT
    global CONF_START_ID, CONF_END_ID, CONF_BUG_ID, CONF_DATA_SET
    print("[DRIVER] Running experiment driver")
    read_arg(arg_list)
    clone_repo()
    # 加载实验数据
    load_experiment()
    create_directories()
    DIR_EXPERIMENT = CONF_DATA_PATH + "/backport/" + REPO_PROGRAM
    if CONF_DATA_SET == "cve-data.json":
        DIR_EXPERIMENT = CONF_DATA_PATH + "/backport/" + REPO_PROGRAM+"-cve"
    sorted_experiment_list = sorted(experiment_list, key=lambda tup: tup['id'])
    # print(sorted_experiment_list)
    for experiment_item in sorted_experiment_list:
        index = int(experiment_item['id'])

        tag_id = None
        if "cve-id" in experiment_item.keys():
            tag_id = experiment_item["cve-id"]
            # print(tag_id)
        '''
        各种配置,会出问题
        if CONF_START_ID:
            if index < CONF_START_ID:
                continue
        if CONF_BUG_ID:
            if index != CONF_BUG_ID:
                continue
        if CONF_END_ID:
            if index >= CONF_END_ID:
                break
        if CONF_BUG_ID_LIST:
            if str(index) not in CONF_BUG_ID_LIST:
                continue
        '''
        
        experiment_name = "Experiment-" + str(index) + "\n-----------------------------"
        print(experiment_name)
        '''原有的commit信息
        fix_parent = str(experiment_item['pa'])
        fix_commit = str(experiment_item['pb'])
        target_bug_commit = str(experiment_item['pc'])
        target_fix_commit = str(experiment_item['pe'])
        '''

        fix_commit = str(experiment_item['pa'])
        fix_parent = ""
        target_commit = str(experiment_item['pc'])

        module_a = None
        module_c = None
        if 'ma' in experiment_item.keys():
            module_a = str(experiment_item['ma'])
        if 'mc' in experiment_item.keys():
            module_c = str(experiment_item['mc'])
        # print(fix_parent)
        commit_list = (fix_commit,fix_parent, target_commit)

        print("\t[META-DATA] Pa: " + fix_commit)
        print("\t[META-DATA] Pb: " + fix_parent)
        print("\t[META-DATA] Pc: " + target_commit)
        # print("\t[META-DATA] Pe: " + target_fix_commit)
        if module_a is not None:
            print("\t[META-DATA] Module-a: " + module_a)
        if module_c is not None:
            print("\t[META-DATA] Module-c: " + module_c)

        conf_file_path = ''

        if not CONF_SKIP_SETUP:
            commit_list = setup_each(DIR_EXPERIMENT, index, commit_list)
            conf_file_path = write_conf_file(DIR_EXPERIMENT, module_a, module_c, index, commit_list)   

        if not CONF_ONLY_SETUP:
            ret_code = evaluate(conf_file_path, index)
            log_file_path = "/FixMorph/logs/linux-" + str(index) + "/log-latest"
            if CONF_DATA_SET == "cve-data.json":
                log_file_path = "/FixMorph/logs/linux-cve-" + str(index) + "/log-latest"
            if CONF_ANALYSIS_MODE:
                if int(ret_code) != 0:
                    if "--analyse-n" in CONF_TOOL_PARAMS:
                        CONF_TOOL_PARAMS = "--analyse-b-n"
                    evaluate(conf_file_path, index)
                    CONF_TOOL_PARAMS = "--analyse-n"
            analyse_result(index, log_file_path)
        comparison_result_file = "/FixMorph/output/"+ REPO_PROGRAM + "-" + str(index) + "/comparison-result"
        if CONF_DATA_SET == "cve-data.json":
            comparison_result_file = "/FixMorph/output/"+REPO_PROGRAM + "-cve-" + str(index) + "/comparison-result"
        if os.path.isfile(comparison_result_file):
            with open(comparison_result_file, "r") as result_file:
                content = result_file.readline()
                if "IDENTICAL" in content:
                    COUNT_IDENTICAL = COUNT_IDENTICAL + 1

        COUNT_EXPERIMENT = COUNT_EXPERIMENT + 1
        print("experiment count: " + str(COUNT_EXPERIMENT))
        print("success count: " + str(COUNT_SUCCESS))
        print("identical count: " + str(COUNT_IDENTICAL))
        print("failure count: " + str(COUNT_FAILURES))
        print("build error count: " + str(COUNT_BUILD_FAILED))
        print("verify error count: " + str(COUNT_VERIFY_FAILED))
        print("runtime error count: " + str(COUNT_RUNTIME_ERRORS) + "\n\n")

    write_as_json(list_other_failed, "fail_list_other")
    write_as_json(list_build_failed, "fail_list_build")
    write_as_json(list_verify_failed, "fail_list_verify")
    write_as_json(list_success, "success_list")

if __name__ == "__main__":
    import sys

    try:
        run(sys.argv[1:])
    except KeyboardInterrupt as e:
        print("[DRIVER] Program Interrupted by User")
        exit()