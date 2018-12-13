# -*- coding: UTF-8 -*-
"""User Agent Tests"""
from os.path import join

import pytest

from hdx.utilities.loader import LoadError
from hdx.utilities.useragent import UserAgent, UserAgentError
from hdx.utilities.version import get_utils_version


class TestUserAgent:
    @pytest.fixture(scope='class')
    def user_agent_config_yaml(self, configfolder):
        return join(configfolder, 'user_agent_config.yml')

    @pytest.fixture(scope='class')
    def user_agent_config2_yaml(self, configfolder):
        return join(configfolder, 'user_agent_config2.yml')

    @pytest.fixture(scope='class')
    def user_agent_config3_yaml(self, configfolder):
        return join(configfolder, 'user_agent_config3.yml')

    @pytest.fixture(scope='class')
    def empty_yaml(self, configfolder):
        return join(configfolder, 'empty.yml')

    @pytest.fixture(scope='class')
    def user_agent_config_wrong_yaml(self, configfolder):
        return join(configfolder, 'user_agent_config_wrong.yml')

    def test_user_agent(self, monkeypatch, user_agent_config_yaml, user_agent_config2_yaml, user_agent_config3_yaml,
                        empty_yaml, user_agent_config_wrong_yaml):
        version = get_utils_version()
        UserAgent.configure(user_agent_config_yaml=user_agent_config_yaml)
        assert UserAgent.get() == 'lala:HDXPythonUtilities/%s-myua' % version
        UserAgent.configure(user_agent_config_yaml=user_agent_config2_yaml)
        assert UserAgent.get() == 'HDXPythonUtilities/%s-myuseragent' % version
        UserAgent.configure(user_agent_config_yaml=user_agent_config3_yaml, user_agent_lookup='lookup')
        assert UserAgent.get() == 'HDXPythonUtilities/%s-mylookupagent' % version
        UserAgent.configure(user_agent_config_yaml=user_agent_config3_yaml, user_agent_lookup='lookup2')
        assert UserAgent.get() == 'HDXPythonUtilities/%s-mylookupagent2' % version
        UserAgent.clear()
        assert UserAgent.get(user_agent='my_ua', preprefix='papa') == 'papa:HDXPythonUtilities/%s-my_ua' % version
        with pytest.raises(UserAgentError):
            UserAgent.configure(user_agent_config_yaml=user_agent_config3_yaml, user_agent_lookup='fail')
        with pytest.raises(LoadError):
            UserAgent.configure(user_agent_config_yaml=empty_yaml)
        with pytest.raises(UserAgentError):
            UserAgent.configure(user_agent_config_yaml=user_agent_config_wrong_yaml)
        with pytest.raises(UserAgentError):
            UserAgent.configure()
        UserAgent.clear()
        with pytest.raises(UserAgentError):
            UserAgent.get()
        my_user_agent = 'lala'
        monkeypatch.setenv('USER_AGENT', my_user_agent)
        assert UserAgent.get() == 'HDXPythonUtilities/%s-%s' % (version, my_user_agent)
        my_preprefix = 'haha'
        monkeypatch.setenv('PREPREFIX', my_preprefix)
        assert UserAgent.get() == '%s:HDXPythonUtilities/%s-%s' % (my_preprefix, version, my_user_agent)
        my_prefix = 'HDXPythonLibrary/%s' % version
        assert UserAgent.get(prefix=my_prefix) == '%s:%s-%s' % (my_preprefix, my_prefix, my_user_agent)
