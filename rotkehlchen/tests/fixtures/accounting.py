import errno
import os

import pytest

from rotkehlchen.accounting.accountant import Accountant
from rotkehlchen.constants import YEAR_IN_SECONDS
from rotkehlchen.history import PriceHistorian
from rotkehlchen.inquirer import Inquirer

TEST_HISTORY_DATA_START = "01/01/2015"


@pytest.fixture
def accounting_data_dir():
    """For accounting we have a dedicated test data dir so that it's easy to
    cache the results of the historic price queries also in Travis"""
    home = os.path.expanduser("~")
    if 'TRAVIS' in os.environ:
        data_directory = os.path.join(home, '.cache', '.rotkehlchen-test-dir')
    else:
        data_directory = os.path.join(home, '.rotkehlchen', 'tests_data_directory')

    try:
        os.makedirs(data_directory)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    return data_directory


@pytest.fixture
def price_historian(accounting_data_dir, inquirer):
    return PriceHistorian(
        data_directory=accounting_data_dir,
        history_date_start=TEST_HISTORY_DATA_START,
        inquirer=inquirer,
    )


@pytest.fixture
def profit_currency():
    return 'EUR'


@pytest.fixture
def accounting_create_csv():
    return False


@pytest.fixture
def accounting_ignored_assets():
    return []


@pytest.fixture
def accounting_include_crypto2crypto():
    return True


@pytest.fixture
def accounting_taxfree_after_period():
    return YEAR_IN_SECONDS


@pytest.fixture
def accounting_include_gas_costs():
    return True


@pytest.fixture
def accountant(
        price_historian,
        profit_currency,
        accounting_data_dir,
        accounting_create_csv,
        accounting_ignored_assets,
        accounting_include_crypto2crypto,
        accounting_taxfree_after_period,
        accounting_include_gas_costs,
):
    return Accountant(
        price_historian=price_historian,
        profit_currency=profit_currency,
        user_directory=accounting_data_dir,
        create_csv=accounting_create_csv,
        ignored_assets=accounting_ignored_assets,
        include_crypto2crypto=accounting_include_crypto2crypto,
        taxfree_after_period=accounting_taxfree_after_period,
        include_gas_costs=accounting_include_gas_costs,
    )


@pytest.fixture
def inquirer(accounting_data_dir):
    return Inquirer(data_dir=accounting_data_dir, kraken=None)
