from kafka import KafkaConsumer
import sys
# Configuração do consumidor Kafka
consumer = KafkaConsumer(
    'appointments',                   # Nome do tópico
    group_id='my_consumer_group',  # Grupo de consumidores
    bootstrap_servers=['kafka:9092'],  # Endereço do servidor Kafka
    auto_offset_reset='earliest'   # Começar do primeiro offset
)
# Função para processar as mensagens
def consume_messages():
    try:
        for message in consumer:
            # Processa a mensagem recebida
            print(f"Recebido: {message.value.decode('utf-8')}")
    except KeyboardInterrupt:
        print("Interrompido pelo usuário.")
    finally:
        # Fecha o consumidor
        consumer.close()
if __name__ == "__main__":
    consume_messages()