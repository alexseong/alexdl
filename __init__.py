is_simple_core = False

if is_simple_core:
	from alexdl.core_simple import Variable
	from alexdl.core_simple import Function
	from alexdl.core_simple import using_config
	from alexdl.core_simple import no_grad
	from alexdl.core_simple import as_array
	from alexdl.core_simple import as_variable
	from alexdl.core_simple import setup_variable
else:
    from alexdl.core import Variable
#    from alexdl.core import Parameter
    from alexdl.core import Function
    from alexdl.core import using_config
    from alexdl.core import no_grad
#    from alexdl.core import test_mode
    from alexdl.core import as_array
    from alexdl.core import as_variable
    from alexdl.core import setup_variable
    from alexdl.core import Config
#    from alexdl.layers import Layer
#    from alexdl.models import Model
#    from alexdl.datasets import Dataset
#    from alexdl.dataloaders import DataLoader
#    from alexdl.dataloaders import SeqDataLoader

#     import alexdl.datasets
#     import alexdl.dataloaders
#     import alexdl.optimizers
#     import alexdl.functions
#     import alexdl.functions_conv
#     import alexdl.layers
#     import alexdl.utils
#     import alexdl.cuda
#     import alexdl.transforms

setup_variable()
__version__ = '0.0.13'