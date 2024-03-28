"""
API methods to execute http queries
"""
import requests


def get(url, params=None, headers=None):
    """
    Execute Get request
    """
    response = requests.get(
        url=url,
        params=params or {},
        headers=headers or {},
    )
    return response.json()
