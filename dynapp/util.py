import click, urllib2, time, json

FTC_LAST_COMMIT_URL = 'https://api.github.com/repos/ftctechnh/ftc_app/git/refs/heads/master'
FTC_TAGS_URL = 'https://api.github.com/repos/ftctechnh/ftc_app/tags'
CACHED_VERSION = ''


def get_version():
    global CACHED_VERSION
    if not CACHED_VERSION:
        try:
            last_commit = json.loads(get_url_retry(FTC_LAST_COMMIT_URL))['object']['sha']
            tags = json.loads(get_url_retry(FTC_TAGS_URL))
            for item in tags:
                if item['commit']['sha'] != last_commit:
                    continue
                CACHED_VERSION = item['name']
                info('Version identified as: {0}'.format(CACHED_VERSION))
        except:
            pass

        if not CACHED_VERSION:
            info('Version could not be discovered!')
            CACHED_VERSION = click.prompt('Please enter in a version [1.0.0]', type=str)
    return CACHED_VERSION


def info(*text):
    click.echo('{0} {1}'.format(click.style('==>', fg='blue'), ' '.join(text)))


def error(*text):
    formatted_text = click.style(' '.join(text), fg='red')
    info(formatted_text)
    raise Exception(formatted_text)


def get_url_retry(url, attempt=1, max_attempts=3):
    try:
        return urllib2.urlopen(url).read()
    except Exception, e:
        if attempt <= max_attempts:
            delay = 3 * attempt
            info('Failed to retrieve resource... Retry in: {0}(s)'.format(delay))
            time.sleep(delay)
            return get_url_retry(url, attempt + 1)
        else:
            error("Failed to retrieve resource!", e.message)
