
API开发实例：通过glance api下载image

We issue a GET request to http://glance.example.com/v1/images/71c675ab-d94f-49cd-a114-e12490b328d9 to 
retrieve metadata for that image as well as the image itself encoded into the response body.

1：获取参数
----------------------------------+---------+
[root@train swift]# openstack token issue
+------------+----------------------------------+
| Field      | Value                            |
+------------+----------------------------------+
| expires    | 2016-08-15T06:26:11.875636Z      |
| id         | 06b50f0299fc402eb3eaa96bf98d8399 |
| project_id | 466b6504fd454107b5221c3a7b4454ba |
| user_id    | 026b050e5cad4e2aaf1f8dc11693bc69 |
+------------+----------------------------------+

[root@train swift]# glance image-list

2：编写代码
import tempfile
import os
from nova import image
from nova import context as nova_ctxt
from oslo_utils import fileutils
IMAGE_API = image.API()
image_href = "http://192.168.1.102:9292/v2/image/54b3b0eb-c7a8-4127-9130-60ed5423a0a6"
data, path = tempfile.mkstemp(dir=“/root/“, prefix='test_')
os.close(data)
context=nova_ctxt.RequestContext(auth_token='gAAAAABY0-qXyZCiAhwPwtYcWkZtZDppOB67yhMJOTgIBqXWXhGHcu_qUWNHQafzmdJQRp9ZwDTTs5xebIQnM9PuZkdnPN2KxWzrl5E2bui0OOVw_ZidFngpTEQOyDe-M5iWZChIcs-agZc_V7EPWeXaZjnF9gPUHsOWCeLnCgOECSTtyIS0s6o',
         is_admin=True,
         project_id='1fbeb32d68694371ac868cfa9475d95f',
         user_id='74c43d0c742c41b48db18c665b51317e',
         project_name='admin')
with fileutils.remove_path_on_error(path):
    IMAGE_API.download(context, image_href, dest_path=path)

3：检查下载的image
[root@train home]# qemu-img info test_DBto7r
image: test_DBto7r
file format: qcow2
virtual size: 39M (41126400 bytes)
disk size: 13M
cluster_size: 65536
Format specific information:
compat: 0.10
