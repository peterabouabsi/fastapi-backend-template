from typing import Optional

from .setup import AppSettings

# Singleton instance of AppSettings
app_settings: Optional[AppSettings]

async def load_app_settings() -> None:
    """
    Load AppSettings into the singleton.
    Must be called at application startup.
    """
    global app_settings
    app_settings = AppSettings()

    ### actions to perform after loading settings
    # 1. [Optional] Load postgres credentials from aws secrets manager
    # await __app_settings.load_pg_creds() 

    # 2. [Optional] ...
    # ....

def get_app_settings() -> AppSettings:
    """
    Retrieve the loaded AppSettings singleton.
    Raises an error if settings are not yet loaded.
    """
    global app_settings
    if app_settings is None:
        raise RuntimeError("App settings are not loaded yet. Call load_app_settings() first.")
    return app_settings