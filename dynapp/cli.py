import click, json
from modules import get_modules
from util import info, get_url_retry
from githubauth import init_github

FTC_LAST_COMMIT_URL = 'https://api.github.com/repos/ftctechnh/ftc_app/git/refs/heads/master'
FTC_TAGS_URL = 'https://api.github.com/repos/ftctechnh/ftc_app/tags'

class Task(object):
    def __init__(self, name):
        self.name = name

    def log_status(self, status, more_info=''):
        more_info = '[{0}]'.format(more_info) if len(more_info) > 0 else more_info
        click.echo('{0}: {1} {2}'.format(click.style(status + ' Task', bold='True'), click.style(self.name, fg='blue'), more_info))

    def __call__(self, original_func):
        def wrapper(*args, **kwargs):
            self.log_status('Executing')
            try:
                original_func(*args, **kwargs)
            except Exception, e:
                self.log_status('Failed', repr(e))
                return
            self.log_status('Completed')

        return wrapper



@click.group()
def main():
    """
    The Dynapp-Updater handles all resources within the repository and ensures they are using all the latest FTC materials
    It automatises a lot of processes within a python module to reduce wasted time when updating.
    """
    pass


@main.command('reset', short_help='Wipe the current sumbodules if an update fails or if changes want to be ignored')
@Task('Reset')
def reset():
    for module in get_modules():
        module.reset()


@main.command('update', short_help='Download all required resources and then override the old sources')
@click.option('--username', '-u', prompt=True, help='A users Github username for API access')
@click.option('--password', '-p', prompt=True, hide_input=True, help='A users Github password for API access')
@Task('Update')
def update(username, password):
    info('Searching for version...')
    version = ''
    try:
        last_commit = json.loads(get_url_retry(FTC_LAST_COMMIT_URL))['object']['sha']
        tags = json.loads(get_url_retry(FTC_TAGS_URL))
        for item in tags:
            if item['commit']['sha'] != last_commit:
                continue
            version = item['name']
            info('Version identified as: {0}'.format(version))
    except:
        pass

    if not version:
        info('Version could not be discovered!')
        version = click.prompt('Please enter in a version [1.0.0]', type=str)

    init_github(username, password)
    for module in get_modules():
        module.update(version)


@main.command('publish', short_help='Publish all changes to the Github Repository')
@Task('Publish')
def publish():
    click.echo('Welcome to: {0}'.format(click.style('Publish', fg='blue', bold=True)))
