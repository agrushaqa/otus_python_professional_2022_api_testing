from yaml_config import YamlConfig


class TestYamlConfig:
    def test_read_str(self, configfile):
        config = YamlConfig().read(configfile)
        assert config['redis']['host'] == "127.0.0.2"

    def test_read_multiplication(self, configfile):
        config = YamlConfig().read(configfile)
        assert eval(config['redis']['period']) == 365 * 70

    def test_read_int(self, configfile):
        config = YamlConfig().read(configfile)
        assert config['redis']['gender'] == 2
        assert isinstance(config['redis']['gender'], int)
