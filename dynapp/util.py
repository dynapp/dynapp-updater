import click, urllib2, time


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
