
description = 'Verify the user can edit page code and save it'

apps = {'appname': '1', 'apppath': '2', 'appPackagename': '3', 'appActivityname': '4'}

def setup(self):
    self.desired_caps = {}
    self.desired_caps['platformName'] = 'Android'
    self.desired_caps['deviceName'] = 'KVD6JZ7999999999' 
    self.desired_caps['platformVersion'] = '5.0.2'
    self.desired_caps['app'] = '2'
    self.desired_caps['appPackage'] = '3'
    self.desired_caps['appActivity'] = '4'
    self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', self.desired_caps)

def test(data):
    pass


def teardown(data):
    pass
