class Config:
    enable_backprop = True

class Variable:
    __array_priority__ = 200
    
    def __init__(self, data, name=None):
        if data is not None:
            if not isinstance(data, np.ndarray):
                raise TypeError('{} type is not supported'.format(type(data)))
        
        self.data = data
        self.name = name
        self.grad = None
        self.creator = None
        self.generation = 0
        
    def set_creator(self, func):
        self.creator = func
        self.generation = func.generation + 1
        
    def backward(self, retain_grad=False):
        if self.grad is None:
            self.grad = np.ones_like(self.data)
        
        funcs = []
        seen_set = set()
        
        def add_func(f):
            if f not in seen_set:
                funcs.append(f)
                seen_set.add(f)
                funcs.sort(key=lambda x: x.generation)
                
        add_func(self.creator)
        
        while funcs:
            f = funcs.pop()
            #gys = [output.grad for output in f.outputs]
            gys = [output().grad for output in f.outputs]
            gxs = f.backward(*gys)
            if not isinstance(gxs, tuple):
                gxs = (gxs,)
                
            for x, gx in zip(f.inputs, gxs):
                if x.grad is None:
                    x.grad = gx
                else:
                    x.grad = x.grad + gx
                
                if x.creator is not None:
                    add_func(x.creator)
                    
            if not retain_grad:
                for y in f.outputs:
                    y().grad = None
                    
    def cleargrad(self):
        self.grad = None
     
    @property
    def shape(self):
        return self.data.shape
    
    @property
    def ndim(self):
        return self.data.ndim
    
    @property
    def size(self):
        return self.data.size
    
    @property
    def dtype(self):
        return self.data.dtype
    
    def __len__(self):
        return len(self.data)
    
    def __repr__(self):
        if self.data is None:
            return 'variable(None)'
        
        p = str(self.data).replace('\n', '\n' + ' ' * 9)
        return 'variable(' + p + ')'

class Function:
    def __call__(self, *inputs):
        inputs = [as_variable(x) for x in inputs]
        
        xs = [x.data for x in inputs]
        ys = self.forward(*xs)
        if not isinstance(ys, tuple):
            ys = (ys,)
        outputs = [Variable(as_array(y)) for y in ys]
        
        if Config.enable_backprop:
            self.generation = max([x.generation for x in inputs])
            for output in outputs:
                output.set_creator(self)

            self.inputs = inputs
            self.outputs = [weakref.ref(output) for output in outputs]
        
        return outputs if len(outputs) > 1 else outputs[0]
    
    def forward(self, xs):
        raise NotImplementedError()
        
    def backward(self, gy):
        raise NotImplementedError()

class Add(Function):
    def forward(self, x0, x1):
        y = x0 + x1
        return y
    
    def backward(self, gy):
        return gy, gy
    

class Mul(Function):
    def forward(self, x0, x1):
        y = x0 * x1
        return y
    
    def backward(self, gy):
        x0, x1 = self.inputs[0].data, self.inputs[1].data
        return gy * x1, gy * x0

class Neg(Function):
    def forward(self, x):
        return -x
    
    def backward(self, gy):
        return -gy

def add(x0, x1):
    if not isinstance(x0, np.ndarray):
        x0 = as_array(x0)
        
    if not isinstance(x1, np.ndarray):
        x1 = as_array(x1)
        
    return Add()(x0, x1)

def mul(x0, x1):
    if not isinstance(x0, np.ndarray):
        x0 = as_array(x0)
        
    if not isinstance(x1, np.ndarray):
        x1 = as_array(x1)
    return Mul()(x0, x1)

def neg(x):
    return Neg()(x)

Variable.__add__ = add
Variable.__radd__ = add
Variable.__mul__ = mul
Variable.__rmul__ = mul
Variable.__neg__ = neg