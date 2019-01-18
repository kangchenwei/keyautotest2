
description = 'Verify the user can access a page by clicking on it in the page list.'

apps = {}

def setup(self):
    self.desired_caps = {}
    self.desired_caps['platformName'] = 'Android'
    self.desired_caps['deviceName'] = 'KVD6JZ7999999999' 
    self.desired_caps['platformVersion'] = '5.0.2'
    self.desired_caps['app'] = test/kuaikan.apk
    self.desired_caps['appPackage'] = com.kuaikanmanhua
    self.desired_caps['appActivity'] = com.kuaikanmanhua
    self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', self.desired_caps)
