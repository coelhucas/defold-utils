import logging
import subprocess
import sys
import os
import configparser

current_platform = os.uname().sysname

PLATFORMS = {
    'macos': 'Darwin'
}

DEFAULT_DEFOLD_PATH: dict[str, str] = {
    PLATFORMS['macos']: '/Applications/Defold.app'
}

DEFOLD_PROCESS = {
    PLATFORMS['macos']: 'Defold'
}[current_platform]

defold_path = DEFAULT_DEFOLD_PATH[current_platform]

logger = logging.getLogger("defold-utility")
logger.propagate = False

is_macos = current_platform == PLATFORMS['macos']
defold_resources_path = os.path.join(defold_path, 'Contents', 'Resources') if is_macos else defold_path
defold_config_path = os.path.join(defold_resources_path, 'config')

def is_defold_running():
    args =  f"pgrep -l {DEFOLD_PROCESS} | awk '{{ print $2 }}'"
    result = subprocess.run([args], shell=True, stdout=subprocess.PIPE)

    return bool(result.stdout)

if os.path.exists(defold_config_path):
    config = configparser.ConfigParser()
    config.read(defold_config_path)

    # In Python, if os.path.join has two 'absolute' paths (e.g.: '/SomePath1', '/SomePath2') any path before the last absolute is removed.
    # That's why we're adding os.path.sep into some replaces.
    jdk_path = os.path.join(defold_resources_path, config['launcher']['jdk'].replace('${bootstrap.resourcespath}' + os.path.sep, config['bootstrap']['resourcespath']))
    java_bin = os.path.normpath(config['launcher']['java'].replace('${launcher.jdk}', jdk_path))
    jar_bin = java_bin.replace(os.path.sep + 'java', os.path.sep + 'jar')
    editor_jar = os.path.join(defold_resources_path, config['launcher']['jar'].replace('${bootstrap.resourcespath}' + os.path.sep, config['bootstrap']['resourcespath']).replace('${build.editor_sha1}', config['build']['editor_sha1']))

    cwd  = os.path.normcase(os.path.join(os.getcwd(), 'game.project'))

    if is_defold_running():
        cmd = f"osascript -e 'activate application \"Defold\"'"
        subprocess.run([cmd], shell=True)
        logger.info("Engine already open. Activating it...")
    else:
        cmd = f"open '{defold_path}' '{cwd}'"
        subprocess.run([cmd], shell=True)
        logger.info("Opening engine...")
else:
    error_message = f"Engine not found at {defold_path}"
    logger.error(error_message)
    raise Exception(error_message)
