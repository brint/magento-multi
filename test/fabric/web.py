import re
from fabric.api import env, run, hide, task
from envassert import detect, file, group, package, port, process, service, \
    user


def magento_is_responding():
    with hide('running', 'stdout'):
        homepage = run("wget --quiet --output-document - --header='Host: example.com' http://localhost/")
        if re.search('Magento Demo Store', homepage):
            return True
        else:
            return False


@task
def check():
    env.platform_family = detect.detect()

    assert file.exists('/var/www/vhosts/example.com/.configured'), '.configured did not exist'

    assert port.is_listening(80), 'port 80 is not listening'
    assert port.is_listening(443), 'port 443 is not listenging'
    assert port.is_listening(9001), 'port 9001 is not listening'

    assert user.exists("magento"), 'magento user does not exist'

    assert process.is_up("nginx"), 'nginx is not running'
    assert process.is_up("php5-fpm"), 'php5-fpm is not running'

    assert service.is_enabled("nginx"), 'nginx service not enabled'
    assert service.is_enabled("php5-fpm"), 'php5-fpm service not enabled'

    assert magento_is_responding(), 'Magento did not respond as expected.'
