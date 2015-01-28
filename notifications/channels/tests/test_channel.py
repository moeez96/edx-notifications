"""
All tests regarding channel.py
"""

from django.test import TestCase
from django.test.utils import override_settings
from django.core.exceptions import ImproperlyConfigured

from notifications.channels.channel import (
    get_notification_channel,
    reset_notification_channels,
    BaseNotificationChannelProvider,
)

from notifications.channels.durable import BaseDurableNotificationChannel

from notifications.data import (
    NotificationType,
)

# list all known channel providers
_NOTIFICATION_CHANNEL_PROVIDERS = {
    'default': {
        'class': 'notifications.channels.durable.BaseDurableNotificationChannel',
        'options': {
            'display_name': 'channel_default',
            'display_description': 'channel_description_default',
        }
    },
    'channel1': {
        'class': 'notifications.channels.durable.BaseDurableNotificationChannel',
        'options': {
            'display_name': 'channel_name1',
            'display_description': 'channel_description1',
        }
    },
    'channel2': {
        'class': 'notifications.channels.durable.BaseDurableNotificationChannel',
        'options': {
            'display_name': 'channel_name2',
            'display_description': 'channel_description2',
        }
    },
    'channel3': {
        'class': 'notifications.channels.durable.BaseDurableNotificationChannel',
        'options': {
            'display_name': 'channel_name3',
            'display_description': 'channel_description3',
        }
    },
    'channel4': {
        'class': 'notifications.channels.durable.BaseDurableNotificationChannel',
        'options': {
            'display_name': 'channel_name4',
            'display_description': 'channel_description4',
        }
    },
    'channel5': {
        'class': 'notifications.channels.durable.BaseDurableNotificationChannel',
        'options': {
            'display_name': 'channel_name5',
            'display_description': 'channel_description5',
        }
    },
    'channel6': {
        'class': 'notifications.channels.durable.BaseDurableNotificationChannel',
        'options': {
            'display_name': 'channel_name6',
            'display_description': 'channel_description6',
        }
    },
}

# list all of the mappings of notification types to channel
_NOTIFICATION_CHANNEL_PROVIDER_TYPE_MAPS = {
    '*': 'default',  # default global mapping
    'edx-notifications.*': 'channel1',
    'edx-notifications.channels.*': 'channel2',
    'edx-notifications.channels.tests.*': 'channel3',
    'edx-notifications.channels.tests.test_channel.*': 'channel4',
    'edx-notifications.channels.tests.test_channel.channeltests.*': 'channel5',
    'edx-notifications.channels.tests.test_channel.channeltests.foo': 'channel6'
}


@override_settings(NOTIFICATION_CHANNEL_PROVIDERS=_NOTIFICATION_CHANNEL_PROVIDERS)
@override_settings(NOTIFICATION_CHANNEL_PROVIDER_TYPE_MAPS=_NOTIFICATION_CHANNEL_PROVIDER_TYPE_MAPS)
class ChannelTests(TestCase):
    """
    Tests for channel.py
    """

    def setUp(self):
        """
        Harnessing
        """
        reset_notification_channels()
        self.test_user_id = 1001  # an arbitrary user_id
        self.test_msg_type = NotificationType(
            name='edx-notifications.channels.tests.test_channel.channeltests.foo'
        )

    def test_cannot_create_instance(self):
        """
        BaseNotificationChannelProvider is an abstract class and we should not be able
        to create an instance of it
        """

        with self.assertRaises(TypeError):
            BaseNotificationChannelProvider()  # pylint: disable=abstract-class-instantiated

    def test_get_provider(self):
        """
        Makes sure we get an instance of the registered store provider
        """

        provider = get_notification_channel(self.test_user_id, self.test_msg_type)

        self.assertIsNotNone(provider)
        self.assertTrue(isinstance(provider, BaseDurableNotificationChannel))

        self.assertEqual(provider.name, 'channel6')
        self.assertEqual(provider.display_name, 'channel_name6')
        self.assertEqual(provider.display_description, 'channel_description6')

    @override_settings(NOTIFICATION_CHANNEL_PROVIDERS=None)
    def test_missing_provider_config(self):
        """
        Make sure we are throwing exceptions on poor channel configuration
        """

        with self.assertRaises(ImproperlyConfigured):
            get_notification_channel(self.test_user_id, self.test_msg_type)

    @override_settings(NOTIFICATION_CHANNEL_PROVIDER_TYPE_MAPS=None)
    def test_missing_maps_config(self):
        """
        Make sure we are throwing exceptions on poor channel mappings configuration
        """

        with self.assertRaises(ImproperlyConfigured):
            get_notification_channel(self.test_user_id, self.test_msg_type)

    @override_settings(NOTIFICATION_CHANNEL_PROVIDER_TYPE_MAPS={'edx-notifications.bogus': 'bogus'})
    def test_missing_global_mapping(self):
        """
        Make sure we are throwing exceptions when global mapping is missing
        """

        with self.assertRaises(ImproperlyConfigured):
            get_notification_channel(self.test_user_id, self.test_msg_type)

    @override_settings(NOTIFICATION_CHANNEL_PROVIDER_TYPE_MAPS={'*': 'bogus'})
    def test_bad_mapping(self):
        """
        Make sure we are throwing exceptions when a msg type is mapped to a channel name
        that does not exist
        """

        with self.assertRaises(ImproperlyConfigured):
            get_notification_channel(self.test_user_id, self.test_msg_type)

    @override_settings(NOTIFICATION_CHANNEL_PROVIDERS={"durable": {"class": "foo"}})
    def test_bad_provider_config(self):
        """
        Make sure we are throwing exceptions on poor configuration
        """

        with self.assertRaises(ImproperlyConfigured):
            get_notification_channel(self.test_user_id, self.test_msg_type)
