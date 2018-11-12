
description = 'Verify that the user can log in to Golem web module'

pages = ['login',
         'index']

def setup(data):
    pass

def test(data):
    navigate(data.env.url)
    click(login.login_button)
    send_keys(login.username_input, 'admin')
    send_keys(login.password_input, 'admin')
    click(login.login_button)
    capture('Verify the user is logged in')
    verify_text_in_element(index.title, 'Select a Project')

def teardown(data):
    pass
