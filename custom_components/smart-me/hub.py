class Hub:
    manufacturer = "Smartme"
    
    def __init__(self, deviceid: str, username: str, password: str) -> None:
        self.deviceid = deviceid
        self.username = username
        self.password = password

    @property
    def hub_id(self) -> str:
        """ID for hub."""
        return self.deviceid

    async def test_connection(self) -> bool:
        """Test connectivity to the Dummy hub is OK."""
        return True
