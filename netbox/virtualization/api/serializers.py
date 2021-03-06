from __future__ import unicode_literals

from rest_framework import serializers

from dcim.api.serializers import NestedDeviceRoleSerializer, NestedPlatformSerializer, NestedSiteSerializer
from dcim.constants import IFACE_FF_VIRTUAL, IFACE_MODE_CHOICES
from dcim.models import Interface
from extras.api.customfields import CustomFieldModelSerializer
from ipam.models import IPAddress, VLAN
from tenancy.api.serializers import NestedTenantSerializer
from utilities.api import ChoiceFieldSerializer, ValidatedModelSerializer
from virtualization.constants import VM_STATUS_CHOICES
from virtualization.models import Cluster, ClusterGroup, ClusterType, VirtualMachine


#
# Cluster types
#

class ClusterTypeSerializer(ValidatedModelSerializer):

    class Meta:
        model = ClusterType
        fields = ['id', 'name', 'slug']


class NestedClusterTypeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='virtualization-api:clustertype-detail')

    class Meta:
        model = ClusterType
        fields = ['id', 'url', 'name', 'slug']


#
# Cluster groups
#

class ClusterGroupSerializer(ValidatedModelSerializer):

    class Meta:
        model = ClusterGroup
        fields = ['id', 'name', 'slug']


class NestedClusterGroupSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='virtualization-api:clustergroup-detail')

    class Meta:
        model = ClusterGroup
        fields = ['id', 'url', 'name', 'slug']


#
# Clusters
#

class ClusterSerializer(CustomFieldModelSerializer):
    type = NestedClusterTypeSerializer()
    group = NestedClusterGroupSerializer()
    site = NestedSiteSerializer()

    class Meta:
        model = Cluster
        fields = ['id', 'name', 'type', 'group', 'site', 'comments', 'custom_fields', 'created', 'last_updated']


class NestedClusterSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='virtualization-api:cluster-detail')

    class Meta:
        model = Cluster
        fields = ['id', 'url', 'name']


class WritableClusterSerializer(CustomFieldModelSerializer):

    class Meta:
        model = Cluster
        fields = ['id', 'name', 'type', 'group', 'site', 'comments', 'custom_fields', 'created', 'last_updated']


#
# Virtual machines
#

# Cannot import ipam.api.NestedIPAddressSerializer due to circular dependency
class VirtualMachineIPAddressSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='ipam-api:ipaddress-detail')

    class Meta:
        model = IPAddress
        fields = ['id', 'url', 'family', 'address']


class VirtualMachineSerializer(CustomFieldModelSerializer):
    status = ChoiceFieldSerializer(choices=VM_STATUS_CHOICES)
    cluster = NestedClusterSerializer()
    role = NestedDeviceRoleSerializer()
    tenant = NestedTenantSerializer()
    platform = NestedPlatformSerializer()
    primary_ip = VirtualMachineIPAddressSerializer()
    primary_ip4 = VirtualMachineIPAddressSerializer()
    primary_ip6 = VirtualMachineIPAddressSerializer()

    class Meta:
        model = VirtualMachine
        fields = [
            'id', 'name', 'status', 'cluster', 'role', 'tenant', 'platform', 'primary_ip', 'primary_ip4', 'primary_ip6',
            'vcpus', 'memory', 'disk', 'comments', 'custom_fields', 'created', 'last_updated',
        ]


class NestedVirtualMachineSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='virtualization-api:virtualmachine-detail')

    class Meta:
        model = VirtualMachine
        fields = ['id', 'url', 'name']


class WritableVirtualMachineSerializer(CustomFieldModelSerializer):

    class Meta:
        model = VirtualMachine
        fields = [
            'id', 'name', 'status', 'cluster', 'role', 'tenant', 'platform', 'primary_ip4', 'primary_ip6', 'vcpus',
            'memory', 'disk', 'comments', 'custom_fields', 'created', 'last_updated',
        ]


#
# VM interfaces
#

# Cannot import ipam.api.serializers.NestedVLANSerializer due to circular dependency
class InterfaceVLANSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='ipam-api:vlan-detail')

    class Meta:
        model = VLAN
        fields = ['id', 'url', 'vid', 'name', 'display_name']


class InterfaceSerializer(serializers.ModelSerializer):
    virtual_machine = NestedVirtualMachineSerializer()
    mode = ChoiceFieldSerializer(choices=IFACE_MODE_CHOICES)
    untagged_vlan = InterfaceVLANSerializer()
    tagged_vlans = InterfaceVLANSerializer(many=True)

    class Meta:
        model = Interface
        fields = [
            'id', 'name', 'virtual_machine', 'enabled', 'mac_address', 'mtu', 'mode', 'untagged_vlan', 'tagged_vlans',
            'description',
        ]


class NestedInterfaceSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='virtualization-api:interface-detail')

    class Meta:
        model = Interface
        fields = ['id', 'url', 'name']


class WritableInterfaceSerializer(ValidatedModelSerializer):
    form_factor = serializers.IntegerField(default=IFACE_FF_VIRTUAL)

    class Meta:
        model = Interface
        fields = [
            'id', 'name', 'virtual_machine', 'form_factor', 'enabled', 'mac_address', 'mtu', 'mode', 'untagged_vlan',
            'tagged_vlans', 'description',
        ]
