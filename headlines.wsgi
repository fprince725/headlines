activate_this = '/home/fpenterprisesinc/Envs/env1/bin/activate_this.py'
execfile(activate_this,dict(__file__=activate_this))
import sys
sys.path.insert(0, "/home/fpenterprisesinc/Envs/env1/headlines")
from test_wsgi import app as application
