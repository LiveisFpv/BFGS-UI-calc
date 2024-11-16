from BFGS.BFGS import BFGS
import numpy as np
class api_service():
    def __init__(self):
        self.bfgs = BFGS()
        self.ui_json = {}
        self.func=""
        self.eps=0.001
        self.vars=[]
        self.coords=[]
        self.derivatives=[]
    def parse_json(self,ui_json):
        self.ui_json = ui_json
        self.func = self.ui_json['func']
        self.eps = self.ui_json['epsilon']
        self.vars = self.ui_json['table_func']['vars']
        self.coords = self.ui_json['table_func']['coords']
        self.derivatives = self.ui_json['table_func']['derivatives']
        self.func=self.get_func(self.func)
        
        def derivate_func(self):
            derivatives_func=np.array()
            for i,v in enumerate(self.derivatives):
                derivatives_func=np.append(self.get_func(v))
            def function(x):
                return np.array([derivative(x) for derivative in derivatives_func])
            return function
        
        self.fprime=derivate_func()
    def get_result_BFGS(self):
        res=BFGS(np.array(self.coords),self.func,self.fprime,None,self.eps)
        pass
    def get_func(self,func):
        def string_to_function(expression):
            def function(x):
                return eval(expression)
            return np.frompyfunc(function, len(self.vars), 1)
        return string_to_function(func)