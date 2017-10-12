import tempfile
import os
from nova import image
from nova import context as nova_ctxt
from oslo_utils import fileutils
IMAGE_API = image.API()
image_href = "http://192.168.1.102:9292/v2/image/54b3b0eb-c7a8-4127-9130-60ed5423a0a6"
data, path = tempfile.mkstemp(dir="/root/", prefix='test_')
os.close(data)
context=nova_ctxt.RequestContext(auth_token='gAAAAABZ33equNzRTiLFztFqReNw4M3DKTtOBuYOpCtS5IS7M_VK5yXynxbrskNcZPTJDjZecyaAgCNfo3X4oUw_shOfn5vxlSHoXhVrFgf9gXSshvggYESVgNlgNcCjkn65f8tys-gyxbPGyJSP0Lp0eG3TL54_pNwlCO5a1rxTQqiVHNy9ocw',
         is_admin=True,
         project_id='1fbeb32d68694371ac868cfa9475d95f',
         user_id='74c43d0c742c41b48db18c665b51317e',
         project_name='admin')
with fileutils.remove_path_on_error(path):
    IMAGE_API.download(context, image_href, dest_path=path)
