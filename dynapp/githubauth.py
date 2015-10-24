import urllib2
import base64


class PreemptiveBasicAuthHandler(urllib2.HTTPBasicAuthHandler):
    def http_request(self, req):
        url = req.get_full_url()
        realm = None
        user, pw = self.passwd.find_user_password(realm, url)
        if pw:
            raw = "%s:%s" % (user, pw)
            auth = 'Basic %s' % base64.b64encode(raw).strip()
            req.add_unredirected_header(self.auth_header, auth)
        return req

    https_request = http_request


def init_github(username, password):
    auth_handler = PreemptiveBasicAuthHandler()
    auth_handler.add_password(realm=None, uri='https://api.github.com/', user=username,passwd=password)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
