"""Methods for dealing with test case modules
Test Cases are modules located inside the /tests/ directory
"""
import os
import re
import sys
import importlib
import inspect
import pprint
import xlwt
from ast import literal_eval

from golem.core import (utils,
                        page_object,
                        test_execution,
                        file_manager)
from golem.core import test_data as test_data_module


def _parse_step(step):
    """Parse a step string of a test function (setup, test or teardown)."""
    method_name = step.split('(', 1)[0].strip()
    # if not '.' in method_name:
    #     method_name = method_name.replace('_', ' ')
    # clean_param_list = []
    param_list = []

    params_re = re.compile('\((?P<args>.+)\)')
    params_search = params_re.search(step)
    if params_search:
        params_string = params_search.group('args')
        param_pairs = []
        inside_param = False
        inside_string = False
        string_char = ''
        current_start = 0
        for i in range(len(params_string)):
            is_last_char = i == len(params_string) -1
            is_higher_level_comma = False

            if params_string[i] == '\'':
                if not inside_string:
                    inside_string = True
                    string_char = '\''
                elif string_char == '\'':
                    inside_string = False

            if params_string[i] == '\"':
                if not inside_string:
                    inside_string = True
                    string_char = '\"'
                elif string_char == '\"':
                    inside_string = False

            if params_string[i] == ',' and not inside_param and not inside_string:
                is_higher_level_comma = True

            if params_string[i] in ['(', '{', '[']:
                inside_param = True
            elif inside_param and params_string[i] in [')', '}', ']']:
                inside_param = False

            if is_higher_level_comma:
                param_pairs.append((current_start, i))
                current_start = i + 1
            elif is_last_char:
                param_pairs.append((current_start, i+1))
                current_start = i + 2

        for pair in param_pairs:
            param_list.append(params_string[pair[0]:pair[1]])

        param_list = [x.strip() for x in param_list]
        # for param in param_list:
        #     # if 'data[' in param:
        #     #     data_re = re.compile("[\'|\"](?P<data>.*)[\'|\"]")
        #     #     g = data_re.search(param)
        #     #     clean_param_list.append(g.group('data'))
        #     if '(' in param and ')' in param:
        #         clean_param_list.append(param)
        #     else:
        #         # clean_param_list.append(param.replace('\'', '').replace('"', ''))
        #         clean_param_list.append(param)
    step = {
        'method_name': method_name,
        'parameters': param_list
    }
    return step


def _get_parsed_steps(function_code):
    """Get a list of parsed steps provided the code of a
    test function (setup, test or teardown)
    """
    steps = []
    code_lines = inspect.getsourcelines(function_code)[0]
    code_lines = [x.strip().replace('\n', '') for x in code_lines]
    code_lines.pop(0)
    for line in code_lines:
        if line != 'pass':
            steps.append(_parse_step(line))
    return steps


def get_test_case_content(root_path, project, test_case_name):
    """Parse and return the contents of a Test in
    the following format:
      'description' :  string
      'apps' :        list of pages
      'steps' :        step dictionary
        'setup' :      parsed setup steps
        'test' :       parsed test steps
        'teardown' :   parsed teardown steps
    """
    test_contents = {
        'description': '',
        'apps': {},
        'steps': {
            'setup': [],
            'test': [],
            'teardown': []
        }
    }
    
    # add the 'project' directory to python path
    # TODO
    #sys.path.append(os.path.join(root_path, 'projects', project))
    test_module = importlib.import_module('projects.{0}.tests.{1}'
                                          .format(project, test_case_name))
    print("test_moudle====================", test_module)
    # get description
    description = getattr(test_module, 'description', '')
    
    # get list of pages
    # pages = getattr(test_module, 'pages', [])
    
    # get list of appinfo
    apps = getattr(test_module, 'apps', {})
    print("apps============", apps)
      
    # get setup steps
    setup_steps = []
    setup_function_code = getattr(test_module, 'setup', None)
    if setup_function_code:
        setup_steps = _get_parsed_steps(setup_function_code)
    
    # get test steps
    test_steps = []
    test_function_code = getattr(test_module, 'test', None)
    if test_function_code:
        test_steps = _get_parsed_steps(test_function_code)
    
    # get teardown steps
    teardown_steps = []
    teardown_function_code = getattr(test_module, 'teardown', None)
    if teardown_function_code:
        teardown_steps = _get_parsed_steps(teardown_function_code)

    test_contents['description'] = description
    test_contents['apps'] = apps
    test_contents['steps']['setup'] = setup_steps
    test_contents['steps']['test'] = test_steps
    test_contents['steps']['teardown'] = teardown_steps
    return test_contents


def get_test_case_code(path):
    """Get test case content as a string
    provided the full path to the python file.
    """
    code = ''
    with open(path, encoding='utf-8') as ff:
        code = ff.read()
    return code


def new_test_case(root_path, project, parents, tc_name):
    """Create a new empty test case."""
    test_case_content = (
        "\n"
        "description = ''\n\n"
        "pages = []\n\n"
        "def setup(data):\n"
        "    pass\n\n"
        "def test(data):\n"
        "    pass\n\n"
        "def teardown(data):\n"
        "    pass\n\n")
    errors = []
    # check if a file already exists
    base_path = os.path.join(root_path, 'projects', project, 'tests')
    full_path = os.path.join(base_path, os.sep.join(parents))
    filepath = os.path.join(full_path, '{}.py'.format(tc_name))
    if os.path.isfile(filepath):
        errors.append('A test with that name already exists')
    if not errors:
        # create the directory structure if it does not exist
        if not os.path.isdir(full_path):
            for parent in parents:
                base_path = os.path.join(base_path, parent)
                file_manager.create_directory(path=base_path, add_init=True)
        
        with open(filepath, 'w') as test_file:
            test_file.write(test_case_content)
        print('Test {} created for project {}'.format(tc_name, project))
    return errors


def _format_page_object_string(page_objects):
    """Format page object string to store in test case."""
    po_string = ''
    for page in page_objects:
        po_string = po_string + " '" + page + "',\n" + " " * 8
    po_string = "[{}]".format(po_string.strip()[:-1])
    return po_string

def _format_app_object_string(app_objects):
    """Format app object string to store in test case."""
    app_string = ''
    print("app_objects==============", app_objects)
    for key in app_objects:
        print("6666666666666666666666666", key)
        app_string = app_string + " ' " + key + " ' :" + app_objects[key] + ",\n"+" " * 8
        print("app_string=================" + app_string)
    app_string = "{}".format(app_string)
    return app_string

def _format_description(description):
    """Format description string to store in test case."""
    formatted_description = ''
    description = description.replace('"', '\\"').replace("'", "\\'")
    if '\n' in description:
        desc_lines = description.split('\n')
        formatted_description = 'description = \'\'\''
        for line in desc_lines:
            formatted_description = formatted_description + '\n' + line
        formatted_description = formatted_description + '\'\'\'\n'
    else:
        formatted_description = 'description = \'{}\'\n'.format(description)
    return formatted_description


def _format_data(test_data):
    """Format data string to store in test case."""
    result = '[\n'
    for data_set in test_data:
        result += '    {\n'
        for key, value in data_set.items():
            if not value:
                value = "''"
            result += '        \'{}\': {},\n'.format(key, value)
        result += '    },\n'
    result += ']\n\n'
    return result


def generate_test_case_path(root_path, project, full_test_case_name):
    """Generate full path to a python file of a test case.
    
    full_test_case_name must be a dot path starting from /tests/ dir.
    Example:
      generate_test_case_path('/', 'project1', 'module1.test1')
      -> '/projects/project1/tests/module1/test1.py'
    """
    tc_name, parents = utils.separate_file_from_parents(full_test_case_name)
    test_case_path = os.path.join(root_path, 'projects', project, 'tests',
                                  os.sep.join(parents), '{}.py'.format(tc_name))
    return test_case_path


def generate_test_case_excel_path(root_path, project, full_test_case_name):
    """Generate full path to a python file of a test case.

    full_test_case_name must be a dot path starting from /tests/ dir.
    Example:
      generate_test_case_path('/', 'project1', 'module1.test1')
      -> '/projects/project1/testcaseExcel/module1/test1'
    """
    tc_name, parents = utils.separate_file_from_parents(full_test_case_name)
    test_case_excel_path = os.path.join(root_path, 'projects', project, 'testcaseExcel', os.sep.join(parents))
    return test_case_excel_path, tc_name

def generate_excel(root_path, project, testSteps, casename, appname, apppath, appPackagename, appActivityname):
    test_case_excel_path, tc_name = generate_test_case_excel_path(root_path, project, casename)
    filename = test_case_excel_path
    if not os.path.exists(filename):
        os.makedirs(filename)
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('testcase', cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet('configure', cell_overwrite_ok=True)

    sheet2.write(0, 0, "AppName")
    sheet2.write(0, 1, "AppPath")
    sheet2.write(0, 2, "AppPackageName")
    sheet2.write(0, 3, "AppActivityName")
    sheet2.write(1, 0, appname)
    sheet2.write(1, 1, apppath)
    sheet2.write(1, 2, appPackagename)
    sheet2.write(1, 3, appActivityname)

    sheet.write(0, 0, "Model")
    sheet.write(0, 1, "step description")
    sheet.write(0, 2, "Action")
    sheet.write(0, 3, "FindWay")
    sheet.write(0, 4, "Element")
    sheet.write(0, 5, "Value")

    row_length = 0
    print(testSteps.values())
    #得到字典testStep中的value值：{'setup': [{'action': 'send_text', 'parameters': [{'stepdescribe': '', 'way': '', 'element': '', 'value': ''}]}], 'test': [{'action': 'install_app', 'parameters':
    #[{'stepdescribe': '', 'value': ''}]}], 'teardown': [{'action': 'clear', 'parameters': [{'stepdescribe': '', 'way': '', 'element': ''}]}]}

    steplist = list(testSteps.values()) #将得到的values值转化成list
    print(steplist)
    print(len(steplist))
    for i in range(len(steplist)):
        stepvalue = steplist[i]
        size = len(stepvalue)
        row_length = row_length + size  #遍历list得到总共的action数，存入row中，作为表格行数控制依据

    stepkeys = list(testSteps.keys())

    row = 1
    setup_step = list(testSteps['setup'])
    sheet.write(row, 0, 'Setup')
    for row in range(row, len(setup_step)+1):
        for col in range(1, 7):
            if(col == 2):
                sheet.write(row, col, u'%s' % list(setup_step[row - 1].values())[col-2])
            else:
                parameters = list(setup_step[row - 1].values())[1]
                param_dict = parameters[0]
                param_keys = list(param_dict.keys())
                for i in range(0, len(param_keys)):
                    key = param_keys[i]
                    if(key == "stepdescribe"):
                        sheet.write(row, 1, u'%s' % param_dict[key])
                    elif(key == "way"):
                        sheet.write(row, 3, u'%s' % param_dict[key])
                    elif(key == "element"):
                        sheet.write(row, 4, u'%s' % param_dict[key])
                    elif(key == "value"):
                        sheet.write(row, 5, u'%s' % param_dict[key])

    row = row + 1
    temprow = row
    test_step = list(testSteps['test'])
    sheet.write(row, 0, 'Test')
    for row in range(row, len(test_step)+row):
        for col in range(1, 7):
            if(col == 2):
                sheet.write(row, col, u'%s' % list(test_step[row - temprow].values())[col-2])
            else:
                parameters = list(test_step[row - temprow].values())[1]
                param_dict = parameters[0]
                param_keys = list(param_dict.keys())
                for i in range(0, len(param_keys)):
                    key = param_keys[i]
                    if(key == "stepdescribe"):
                        sheet.write(row, 1, u'%s' % param_dict[key])
                    elif(key == "way"):
                        sheet.write(row, 3, u'%s' % param_dict[key])
                    elif(key == "element"):
                        sheet.write(row, 4, u'%s' % param_dict[key])
                    elif(key == "value"):
                        sheet.write(row, 5, u'%s' % param_dict[key])

    row = row + 1
    temprow = row
    teardown_step = list(testSteps['teardown'])
    sheet.write(row, 0, 'Teardown')
    for row in range(row, len(teardown_step) + row):
        for col in range(1, 7):
            if (col == 2):
                sheet.write(row, col, u'%s' % list(teardown_step[row - temprow].values())[col - 2])
            else:
                parameters = list(teardown_step[row - temprow].values())[1]
                param_dict = parameters[0]
                param_keys = list(param_dict.keys())
                for i in range(0, len(param_keys)):
                    key = param_keys[i]
                    if (key == "stepdescribe"):
                        sheet.write(row, 1, u'%s' % param_dict[key])
                    elif (key == "way"):
                        sheet.write(row, 3, u'%s' % param_dict[key])
                    elif (key == "element"):
                        sheet.write(row, 4, u'%s' % param_dict[key])
                    elif (key == "value"):
                        sheet.write(row, 5, u'%s' % param_dict[key])

    workbook.save(r"%s.xls" % (filename+"\\"+tc_name))


def save_test_case(root_path, project, full_test_case_name, description,
                   app_objects, test_steps, test_data):
    """Save test case contents to file.

    full_test_case_name is a relative dot path to the test
    """
    test_case_path = generate_test_case_path(root_path, project,
                                             full_test_case_name)
    formatted_description = _format_description(description)
    with open(test_case_path, 'w', encoding='utf-8') as f:
        # write description
        f.write('\n')
        f.write(formatted_description)
        f.write('\n')
        # write the list of page
        # f.write('pages = {}\n'.format(_format_page_object_string(page_objects)))
        # f.write('\n')
        f.write('apps = {}\n'.format(app_objects))
        f.write('\n')
        # write test data if required or save test data to external file
        if test_execution.settings['test_data'] == 'infile':
            if test_data:
                pretty = pprint.PrettyPrinter(indent=4, width=1)
                #f.write('data = ' + pretty.pformat(test_data) + '\n\n')
                f.write('data = {}'.format(_format_data(test_data)))
                test_data_module.remove_csv_if_exists(root_path, project, full_test_case_name)
        else:
            test_data_module.save_external_test_data_file(root_path, project,
                                                          full_test_case_name,
                                                          test_data)
        # write the setup function
        f.write('def setup(self):\n')
        if test_steps['setup']:
            #添加appium配置信息
            f.write("    self.desired_caps = {}\n")
            f.write("    self.desired_caps['platformName'] = 'Android'\n")
            f.write("    self.desired_caps['deviceName'] = 'KVD6JZ7999999999' \n")
            f.write("    self.desired_caps['platformVersion'] = '5.0.2'\n")
            f.write("    self.dess['app'] = '" + app_objects['apppath'] + "'\n")
            f.write("    self.desired_caps['appPackage'] = '" + app_objects['appPackagename'] + "'\n")
            f.write("    self.desired_caps['appActivity'] = '" + app_objects['appActivityname'] + "'\n")
            f.write("    self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', self.desired_caps)\n")
            for step in test_steps['setup']:
                step_action = step['action'].replace(' ', '_')
                parameters = step['parameters'][0]
                print("step['parameters'][0]============", parameters)
                if(parameters['way'] != None):
                    way = parameters['way']
                elif (parameters['element'] != None):
                    element = parameters['element']
                elif (parameters['value'] != None):
                    value = parameters['value']
                param_str = ', '.join(way)
                f.write('    {0}({1})\n'.format(step_action, param_str))
        else:
            # 添加appium配置信息
            f.write("    self.desired_caps = {}\n")
            f.write("    self.desired_caps['platformName'] = 'Android'\n")
            f.write("    self.desired_caps['deviceName'] = 'KVD6JZ7999999999' \n")
            f.write("    self.desired_caps['platformVersion'] = '5.0.2'\n")
            f.write("    self.desired_caps['app'] = '" + app_objects['apppath'] + "'\n")
            f.write("    self.desired_caps['appPackage'] = '" + app_objects['appPackagename'] + "'\n")
            f.write("    self.desired_caps['appActivity'] = '" + app_objects['appActivityname'] + "'\n")
            f.write("    self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', self.desired_caps)\n")
        f.write('\n')
        # write the test function
        f.write('def test(data):\n')
        if test_steps['test']:
            for step in test_steps['test']:
                step_action = step['action'].replace(' ', '_')
                parameters = step['parameters'][0]
                print("step['parameters'][0]============", parameters)
                if (parameters['way'] != None):
                    way = parameters['way']
                elif (parameters['element'] != None):
                    element = parameters['element']
                elif (parameters['value'] != None):
                    value = parameters['value']
                param_str = ', '.join(way)
                f.write('    {0}({1})\n'.format(step_action, param_str))
        else:
            f.write('    pass\n')
        f.write('\n\n')
        # write the teardown function
        f.write('def teardown(data):\n')
        if test_steps['teardown']:
            for step in test_steps['teardown']:
                step_action = step['action'].replace(' ', '_')
                parameters = step['parameters'][0]
                print("step['parameters'][0]============", parameters)
                if (parameters['way'] != None):
                    way = parameters['way']
                elif (parameters['element'] != None):
                    element = parameters['element']
                elif (parameters['value'] != None):
                    value = parameters['value']
                param_str = ', '.join(way)
                f.write('    {0}({1})\n'.format(step_action, param_str))
        else:
            f.write('    pass\n')


def save_test_case_code(root_path, project, full_test_case_name,
                        content, table_test_data):
    """Save test case contents string to file.
    full_test_case_name is a relative dot path to the test.
    """
    test_case_path = generate_test_case_path(root_path, project, full_test_case_name)
    with open(test_case_path, 'w', encoding='utf-8') as test_file:
        test_file.write(content)
    # save test data
    if table_test_data:
        #save csv data
        test_data_module.save_external_test_data_file(root_path, project,
                                                      full_test_case_name,
                                                      table_test_data)
    elif test_execution.settings['test_data'] == 'infile':
        # remove csv files
        test_data_module.remove_csv_if_exists(root_path, project, full_test_case_name)


def test_case_exists(workspace, project, full_test_case_name):
    """Test case exists.

    full_test_case_name is a relative dot path to the test.
    """
    test, parents = utils.separate_file_from_parents(full_test_case_name)
    path = os.path.join(workspace, 'projects', project, 'tests',
                        os.sep.join(parents), '{}.py'.format(test))
    return os.path.isfile(path)
