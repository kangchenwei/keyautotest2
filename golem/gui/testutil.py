import inspect
import golem.findways

class KKeyTest_findways:
    __instance = None
    findways = None

    def __new__(cls):
        if KKeyTest_findways.__instance is None:
            KKeyTest_findways.__instance = object.__new__(cls)
        return KKeyTest_findways.__instance

    def _is_module_function(self, mod, func):
        return inspect.isfunction(func) and inspect.getmodule(func) == mod

    @property
    def get_findways(self):
        if not self.findways:
            findways = []
            module = golem.findways

            def is_valid_function(function, module):
                if self._is_module_function(module, function):
                    if not function.__name__.startswith('_'):
                        return True
                return False

            findways_list = [function for function in module.__dict__.values()
                                if is_valid_function(function, module)]

            print("====waywaywaywaywaywaywaywaywaywaywaywaywaywaywaywaywaywaywaywaywayway======================")
            print(findways_list)

            for findways in findways_list:
                # print("action_def=============")
                # print(action_def)
                findways.append(findways)
            self.findways = findways
        
            return self.findways