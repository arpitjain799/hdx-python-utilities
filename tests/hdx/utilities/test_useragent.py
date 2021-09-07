"""User Agent Tests"""
from os.path import join

import pytest

from hdx.utilities.loader import LoadError
from hdx.utilities.useragent import UserAgent, UserAgentError
from hdx.utilities.version import get_utils_version


class TestUserAgent:
    @pytest.fixture(scope="class")
    def user_agent_config_yaml(self, configfolder):
        return join(configfolder, "user_agent_config.yml")

    @pytest.fixture(scope="class")
    def user_agent_config2_yaml(self, configfolder):
        return join(configfolder, "user_agent_config2.yml")

    @pytest.fixture(scope="class")
    def user_agent_config3_yaml(self, configfolder):
        return join(configfolder, "user_agent_config3.yml")

    @pytest.fixture(scope="class")
    def empty_yaml(self, configfolder):
        return join(configfolder, "empty.yml")

    @pytest.fixture(scope="class")
    def user_agent_config_wrong_yaml(self, configfolder):
        return join(configfolder, "user_agent_config_wrong.yml")

    def test_user_agent(
        self,
        monkeypatch,
        user_agent_config_yaml,
        user_agent_config2_yaml,
        user_agent_config3_yaml,
        empty_yaml,
        user_agent_config_wrong_yaml,
    ):
        version = get_utils_version()
        assert (
            UserAgent.get(user_agent_config_yaml=user_agent_config_yaml)
            == f"lala:HDXPythonUtilities/{version}-myua"
        )
        assert (
            UserAgent.get(user_agent_config_yaml=user_agent_config2_yaml)
            == f"HDXPythonUtilities/{version}-myuseragent"
        )
        assert (
            UserAgent.get(
                user_agent_config_yaml=user_agent_config3_yaml,
                user_agent_lookup="lookup",
            )
            == f"HDXPythonUtilities/{version}-mylookupagent"
        )
        assert (
            UserAgent.get(user_agent="my_ua", preprefix="papa")
            == f"papa:HDXPythonUtilities/{version}-my_ua"
        )
        UserAgent.set_global(
            user_agent_config_yaml=user_agent_config3_yaml, user_agent_lookup="lookup2"
        )
        assert UserAgent.get() == f"HDXPythonUtilities/{version}-mylookupagent2"
        UserAgent.clear_global()
        with pytest.raises(UserAgentError):
            UserAgent.get(
                user_agent_config_yaml=user_agent_config3_yaml, user_agent_lookup="fail"
            )
        with pytest.raises(LoadError):
            UserAgent.get(user_agent_config_yaml=empty_yaml)
        with pytest.raises(UserAgentError):
            UserAgent.get(user_agent_config_yaml=user_agent_config_wrong_yaml)
        with pytest.raises(UserAgentError):
            UserAgent.get(user_agent_config_yaml="")
        with pytest.raises(UserAgentError):
            UserAgent.get()
        with pytest.raises(UserAgentError):
            UserAgent._load(prefix="", user_agent_config_yaml="")
        my_user_agent = "lala"
        monkeypatch.setenv("USER_AGENT", my_user_agent)
        assert UserAgent.get() == f"HDXPythonUtilities/{version}-{my_user_agent}"
        my_preprefix = "haha"
        monkeypatch.setenv("PREPREFIX", my_preprefix)
        assert (
            UserAgent.get()
            == f"{my_preprefix}:HDXPythonUtilities/{version}-{my_user_agent}"
        )
        my_prefix = f"HDXPythonLibrary/{version}"
        assert (
            UserAgent.get(prefix=my_prefix)
            == f"{my_preprefix}:{my_prefix}-{my_user_agent}"
        )
        UserAgent.clear_global()
