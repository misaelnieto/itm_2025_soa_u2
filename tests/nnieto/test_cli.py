"""Estas son las pruebas para la interfaz de línea de comandos."""
from click.testing import CliRunner
from webservice.app import main, _find_wsgi_apps


def test_main():
    """Test the webservice runner."""
    runner = CliRunner()
    test = runner.invoke(main, ['--help'])
    assert test.exit_code == 0


def test_find_wsgi_apps():
    """Test that _find_wsgi_apps() recognizes at least two apps."""
    apps = _find_wsgi_apps()
    assert len(apps) >= 2, 'Expected at least 2 wsgi apps'
    assert '/ws/nnieto/alcancia/v1' in apps
    assert '/ws/nnieto/alcancia/v2' in apps
    assert callable(apps['/ws/nnieto/alcancia/v1'])
    assert callable(apps['/ws/nnieto/alcancia/v2'])


