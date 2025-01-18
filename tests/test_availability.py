import sys
import os

# Adicionando o diretório raiz ao caminho de importação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import pytest
from datetime import datetime
from app.models import Availability  # Assumindo que seu modelo está no diretório app.models

# Teste básico para criação de uma disponibilidade
def test_create_availability():
    # Criação de uma instância de Availability com dados fictícios
    availability = Availability(
        doctor_id="doctor123",
        available_times=[datetime(2025, 1, 17, 9, 30)],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Verificando se os dados foram atribuídos corretamente
    assert availability.doctor_id == "doctor123"
    assert availability.available_times == [datetime(2025, 1, 17, 9, 30)]
    assert availability.created_at is not None
    assert availability.updated_at is not None

# Teste de valores padrão
def test_default_values():
    # Criação de uma instância de Availability sem fornecer valores de created_at, updated_at
    availability = Availability(
        doctor_id="doctor456", 
        available_times=[datetime(2025, 1, 18, 15, 00)]
    )

    # Verificando se os valores padrões de created_at e updated_at foram atribuídos corretamente
    assert availability.created_at is not None
    assert availability.updated_at is not None

# Teste de validação de dados (erro de tipo)
def test_invalid_data():
    with pytest.raises(ValueError):  # Esperamos que lance um ValueError se o tipo de dado estiver errado
        Availability(
            doctor_id="doctor123",
            available_times="invalid_times",  # Tipo inválido, deve lançar um erro
            created_at="invalid_date"  # Data inválida, deve lançar um erro
        )
