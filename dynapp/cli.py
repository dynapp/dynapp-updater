import click
import urllib2
import os

class ModuleUpdater:
    def __init__(self, name, git):
        self.name = name
        self.git = git

    def execute(self):
        return


@click.command()
@click.option('--publish', '-p', is_flag=True, help='Publish all submodule changes to github')
@click.option('--update', '-u', is_flag=True, help='Update all modules')
@click.option('--reset', '-r', is_flag=True, help='Revert all changes and redownload submodules')
def main(update, ):
    '''Manages and Updates all the Dynapp Repo's'''
    #greet = 'Howdy' if as_cowboy else 'Hello'
    #click.echo('{0}, {1}.'.format(greet, name))

    click.echo('Welcome to: {0}'.format(click.style('Dynapp-Updater', fg='blue', bold=True)))

