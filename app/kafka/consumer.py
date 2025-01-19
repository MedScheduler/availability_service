import json
import logging
from datetime import datetime
from kafka import KafkaConsumer
from app.database import get_availabilities_by_doctor_id, update_doctor_availability_in_db

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AppointmentConsumer:
    def __init__(self):
        self.kafka_bootstrap_servers = "kafka:9092"
        self.kafka_topic = "appointments"
        self.consumer = KafkaConsumer(
            self.kafka_topic,
            bootstrap_servers=self.kafka_bootstrap_servers,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='earliest'
        )
        logger.info(f"Conectado ao Kafka no servidor {self.kafka_bootstrap_servers}, tópico: {self.kafka_topic}")

    async def consume_events(self, process_appointment_event):
        for message in self.consumer:
            logger.info(f"Mensagem recebida: {message.value}")
            await process_appointment_event(message.value)


async def process_appointment_event(event_data):
    doctor_id = event_data["doctor_id"]
    appointment_time_str = event_data["date"]

    try:
        # Garantir que a string de data esteja em formato ISO antes de converter para datetime
        appointment_time = datetime.fromisoformat(appointment_time_str)
    except ValueError:
        logger.error(f"Erro ao converter data de agendamento: {appointment_time_str}")
        return

    # Buscar as disponibilidades do médico
    availabilities = await get_availabilities_by_doctor_id(doctor_id)

    for availability in availabilities:
        # Verificar se a data de disponibilidade coincide com o agendamento
        for available_time in availability["available_times"]:
            if isinstance(available_time, datetime):
                # Converter datetime para string no formato ISO
                available_time_str = available_time.isoformat()
            else:
                available_time_str = available_time

            if available_time_str == appointment_time_str:
                # Remover o horário da lista de disponíveis
                availability["available_times"].remove(available_time)

                # Atualizar as disponibilidades no banco de dados
                await update_doctor_availability_in_db(doctor_id, {"available_times": availability["available_times"]})

                logger.info(f"Disponibilidade do médico {doctor_id} excluída para o horário {appointment_time}")
                return

    logger.warning(f"Não foi encontrada disponibilidade para o horário {appointment_time} do médico {doctor_id}")


async def main():
    consumer = AppointmentConsumer()
    await consumer.consume_events(process_appointment_event)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())