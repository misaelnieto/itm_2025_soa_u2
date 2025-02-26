"""Pruebas de mi servicio web, etapa 2.

En la etapa 2 ya se implementan las operaciones de depósito y retiro, y se agregan validaciones a los parámetros de las operaciones.

"""
from decimal import Decimal

import pytest
from suds.client import Client as SoapClient


@pytest.fixture
def ws(wsgi_live_server):
    """Fixture que inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    service_url = f'{base_url}/ws/nnieto/alcancia/v2'
    wsdl_url = f'{service_url}?wsdl'
    return SoapClient(wsdl_url)


def test_wsdl_metadata(ws):
    """Test that our server provides valid WSDL metadata."""
    # First check the target namespace is correct. This will fail when you change the tns in the webservice.py
    assert ws.wsdl.tns == ('tns', 'com.noenieto.alcancia')

    # Inspect the service definition
    sd = ws.sd[0]
    assert sd.service.name == 'AlcanciaService'
    # We have one port, named Alcancia, that points to the root of the service ...
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == 'Alcancia2'

    # Has 4 methods, and 11 types
    assert len(svc_port.methods) == 4
    assert len(sd.types) == 13


def test_service_methods(ws):
    """Test that our server provides the expected service methods."""
    # Inicialmente no hay saldo
    assert ws.service.saldo() == Decimal('0')

    # Si intentamos retirar dinero, no debe ser posible
    op = ws.service.retiro(100)
    assert op.status == 'ERROR'
    assert op.message == 'Fondos insuficientes'

    # Si depositamos dinero, el saldo debe ser el depositado
    op = ws.service.deposito(100)
    assert op.status == 'OK'
    assert op.saldo == Decimal('100')
    assert op.message == 'Deposito exitoso'
    assert ws.service.saldo() == Decimal('100')

    # Si intentamos retirar más de lo que hay, no debe ser posible
    op = ws.service.retiro(101)
    assert op.status == 'ERROR'
    assert op.message == 'Fondos insuficientes'

    # Si intentamos retirar lo que hay, debe ser posible
    op = ws.service.retiro(100)
    assert op.status == 'OK'
    assert op.saldo == Decimal('0')
    assert op.message == 'Retiro exitoso'
    assert ws.service.saldo() == Decimal('0')

    # Finalmente, revisemos la lista de movimientos
    m = ws.service.movimientos()
    assert len(m.Movimiento) == 2
    assert m.Movimiento[0].cantidad == Decimal('100')
    assert m.Movimiento[1].cantidad == Decimal('-100')

