import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


# Test for installed packages
def test_nginx_is_installed(host):
    rsyslog = host.package("rsyslog")
    assert rsyslog.is_installed


# Test for the Node user, group and home directory.
def test_node_group(host):
    node_group = host.group("node")
    assert node_group.exists


def test_node_user(host):
    node_user = host.user("node")
    assert node_user.exists


def test_node_home_dir(host):
    node_home_dir = host.file("/home/node")
    assert node_home_dir.exists


def test_node_home_user(host):
    node_home_dir_user = host.file("/home/node").user
    assert node_home_dir_user == "node"


def test_node_home_group(host):
    node_home_dir_group = host.file("/home/node").group
    assert node_home_dir_group == "node"


def test_node_home_mode(host):
    node_home_dir_mode = host.file("/home/node").mode == 0o755
    assert node_home_dir_mode


# Test for the /etc/notejam directory and configuration file
def test_etc_notejam_dir(host):
    etc_notejam_dir = host.file("/etc/notejam")
    assert etc_notejam_dir.is_directory


def test_etc_notejam_dir_user(host):
    etc_notejam_dir_user = host.file("/etc/notejam").user
    assert etc_notejam_dir_user == "root"


def test_etc_notejam_dir_group(host):
    etc_notejam_dir_group = host.file("/etc/notejam").group
    assert etc_notejam_dir_group == "root"


def test_etc_notejam_dir_mode(host):
    etc_notejam_dir_mode = host.file("/etc/notejam").mode == 0o644
    assert etc_notejam_dir_mode


def test_notejam_env_file(host):
    notejam_env_file = host.file("/etc/notejam/notejam-mysql.env")
    assert notejam_env_file


def test_notejam_env_file_user(host):
    notejam_env_file_user = host.file("/etc/notejam/notejam-mysql.env").user
    assert notejam_env_file_user == "root"


def test_notejam_env_file_group(host):
    notejam_env_file_group = host.file("/etc/notejam/notejam-mysql.env").group
    assert notejam_env_file_group == "root"


def test_notejam_env_file_mode(host):
    notejam_env_file_mode = host.file("/etc/notejam/notejam-mysql.env")\
                                .mode == 0o644
    assert notejam_env_file_mode


# Test for the /tmp directory
def test_tmp_dir(host):
    tmp_dir = host.file("/tmp")
    assert tmp_dir.is_directory


def test_tmp_dir_user(host):
    tmp_dir_user = host.file("/tmp").user
    assert tmp_dir_user == "root"


def test_tmp_dir_group(host):
    tmp_dir_group = host.file("/tmp").group
    assert tmp_dir_group == "root"


def test_tmp_dir_mode(host):
    tmp_dir_mode = host.file("/tmp").mode == 0o777
    assert tmp_dir_mode


# Test for NoteJam App
def test_node_modules(host):
    node_modules = host.file("/home/node/app/node_modules")
    assert node_modules.is_directory


def test_node_modules_user(host):
    node_modules_user = host.file("/home/node/app/node_modules").user
    assert node_modules_user == "node"


def test_node_modules_group(host):
    node_modules_group = host.file("/home/node/app/node_modules").group
    assert node_modules_group == "node"


def test_node_modules_mode(host):
    node_modules_mode = host.file("/home/node/app/node_modules").mode == 0o755
    assert node_modules_mode


def test_package_json(host):
    package_json = host.file("/home/node/app/package.json")
    assert package_json.is_file


# Test for RSyslog configuration file
def test_notejam_rsyslog_conf_file(host):
    notejam_rsyslog_conf_file = host.file("/etc/rsyslog.d/notejam-mysql.conf")
    assert notejam_rsyslog_conf_file


def test_notejam_rsyslog_conf_file_user(host):
    notejam_rsyslog_conf_file_user = host.file(
        "/etc/rsyslog.d/notejam-mysql.conf").user
    assert notejam_rsyslog_conf_file_user == "root"


def test_notejam_rsyslog_conf_file_group(host):
    notejam_rsyslog_conf_file_group = host.file(
        "/etc/rsyslog.d/notejam-mysql.conf").group
    assert notejam_rsyslog_conf_file_group == "root"


def test_notejam_rsyslog_conf_file_mode(host):
    notejam_rsyslog_conf_file_mode = host.file(
        "/etc/rsyslog.d/notejam-mysql.conf").mode == 0o644
    assert notejam_rsyslog_conf_file_mode


# Test for Systemd service
def test_notejam_systemd_service_file(host):
    notejam_systemd_service_file = host.file(
        "/etc/systemd/system/notejam-mysql.service")
    assert notejam_systemd_service_file


def test_notejam_systemd_service_file_user(host):
    notejam_systemd_service_file_user = host.file(
        "/etc/systemd/system/notejam-mysql.service").user
    assert notejam_systemd_service_file_user == "root"


def test_notejam_systemd_service_file_group(host):
    notejam_systemd_service_file_group = host.file(
        "/etc/systemd/system/notejam-mysql.service").group
    assert notejam_systemd_service_file_group == "root"


def test_notejam_systemd_service_file_mode(host):
    notejam_systemd_service_file_mode = host.file(
        "/etc/systemd/system/notejam-mysql.service").mode == 0o644
    assert notejam_systemd_service_file_mode
