import click, zipfile, StringIO, commands, json, base64, urllib2
from util import info, error, get_url_retry
from git import *
import shutil
from os import path, getcwd, makedirs

ROBOT_CORE_URL = 'https://raw.githubusercontent.com/ftctechnh/ftc_app/master/FtcRobotController/libs/RobotCore-release.aar'
OPMODE_URL = 'https://api.github.com/repos/ftctechnh/ftc_app/contents/FtcRobotController/src/main/java/com/qualcomm/ftcrobotcontroller/opmodes'
MAVEN_ADD_CMD = 'mvn install:install-file -DgroupId=com.qualcomm -DartifactId=robotcore -Dversion={0} -Dpackaging=jar -Dfile={1} -DlocalRepositoryPath={2}'
OPMODE_WHITELIST = ['package-info.java', 'FtcOpModeRegister.java']

class BaseModule:
    def __init__(self, name, module_dir):
        self.name = name
        self.dir = path.join(getcwd(), 'modules', module_dir)
        self.repo = None

    def init(self):
        if not path.exists(self.dir):
            error('Unable to find module: {0}'.format(self.name))
        click.echo('Executing on Module: {0}'.format(click.style(self.name, fg='blue')))
        self.repo = Repo(self.dir)

    def update(self, version):
        self.init()

    def reset(self):
        self.init()
        info('Attempting to clean...')
        self.repo.git.reset('--hard')
        self.repo.heads.master.checkout()
        self.repo.git.reset('--hard')
        self.repo.git.clean('-xdf')
        info('Data clean was successful!')

        info('Downloading master repository...')
        self.repo.remotes.origin.pull()
        info('Download Complete!')


class RobotCoreModule(BaseModule):
    def __init__(self):
        BaseModule.__init__(self, 'Robot Core', 'robot-core')

    def update(self, version):
        self.init()
        info('Retrieving robot-core...')
        zip_stream = StringIO.StringIO(get_url_retry(ROBOT_CORE_URL))
        robot_core = zipfile.ZipFile(zip_stream).open('classes.jar').read()
        info('Saving robot-core...')
        with open(path.join(self.dir, 'robotcore-latest.jar'), 'wb') as jar:
            jar.write(robot_core)
        info('Robot-core Saved!')

        info('Maven-izing project...')
        status, _ = commands.getstatusoutput(
            MAVEN_ADD_CMD.format(version, path.join(self.dir, 'robotcore-latest.jar'), path.join(self.dir, 'repo')))
        if status != 0:
            error('Maven is not installed!' if status == 32512 else 'Maven failed to install dependency')
        info('Maven sync complete!')

        info('Writing readme...')
        with open('resources/robotcore-template.md', 'r') as template:
            with open(path.join(self.dir, 'README.md'), 'wb') as readme:
                readme.write(template.read().format(version))
        info('Wrote readme!')


class DynappModule(BaseModule):
    def __init__(self):
        BaseModule.__init__(self, 'Dynapp Module (Maven)', 'dynapp-module-maven')

    def github_download(self, url, dir_name, blacklist=None):
        if not blacklist:
            blacklist = []
        if not path.exists(dir_name):
            makedirs(dir_name)
        github_dir = json.loads(get_url_retry(url))
        for item in github_dir:
            if item['type'] == 'file' and item['name'] not in blacklist:
                info('Downloading: {0}'.format(item['name']))
                raw_data = get_url_retry(item['url'])
                with open(path.join(dir_name, item['name']), 'w') as export:
                    decoded_data = base64.b64decode(json.loads(raw_data)['content'])
                    export.write(decoded_data)
            elif item['type'] == 'dir':
                self.github_download(item['url'], path.join(dir_name, item['name']))

    def update(self, version):
        self.init()
        info('Clearing old template code...')
        old_source = path.join(self.dir, 'src/main/java/com')
        if path.exists(old_source):
            shutil.rmtree(path.join(self.dir, 'src/main/java/com'))
        info('Template code cleared!')

        info('Cloning new template code...')
        self.github_download(OPMODE_URL, path.join(self.dir, 'src/main/java/com/qualcomm/opmodes/'), OPMODE_WHITELIST)
        info('Cloned!')


def get_modules():
    return [RobotCoreModule(), DynappModule()]
