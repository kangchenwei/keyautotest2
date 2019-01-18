from golem.browser import element


save_button = ('id', 'save', 'Save button')
preview_button = ('id', 'loadGuiButton', 'Preview button')


def verify_error_message(expected_error):
    error_container = element(id='error-container')
    assert error_container.text == expected_error