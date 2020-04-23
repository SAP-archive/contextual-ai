# configuration for Whitesource
def get_version():
    with open('version.txt') as ver_file:
        version_str = ver_file.readline().rstrip()
    return version_str


config_info = {
   'org_token': '6971b2eec2d3420bad0caf173ec629f6a3c7d3ba63f3445ab99ffdbf1acfb1d0',
   'user_key': 'bcc99c539bd74318977efae53b1e73f30fa7349821984710a50eabf649ade1e7',
   'check_policies': True,
   'product_name': 'SHC - LEO AI BUSVC XAI OD 1.0',
   'force_check_all_dependencies': True,
   'force_update': True,
   'index_url': 'http://nexus.wdf.sap.corp:8081/nexus/content/groups/build.snapshots.pypi/simple/'
}
