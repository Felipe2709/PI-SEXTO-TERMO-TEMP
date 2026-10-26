"""
Gera relatório com as últimas leituras válidas de temperatura e umidade do rádio Meshtastic
e exibe estatísticas agregadas (média, min, max) para documentação e prints do artigo.
"""
import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def obter_leituras(limite=15):
    client = MongoClient(os.environ["MONGO_URI"])
    col = client[os.environ["MONGO_DB"]][os.environ["MONGO_COLLECTION"]]

    # Filtra apenas documentos que possuem medição de temperatura válida
    filtro = {
        "payload_data.sender": "!8fa724e8",
        "payload_data.payload.t": {"$exists": True}
    }

    docs = list(col.find(filtro).sort("_id", -1).limit(limite))[::-1]
    return docs, col

def formatar_relatorio():
    docs, col = obter_leituras(15)

    print("=" * 68)
    print("      FATEC SHUNJI NISHIMURA - PROJETO INTEGRADOR VI (BIG DATA)")
    print("        MONITORAMENTO IOT / MESHTASTIC + MONGODB (DHT11)")
    print("=" * 68)
    print(f"Coleção: {col.full_name} | Total no banco: {col.estimated_document_count()} registros")
    print(f"Rádio emissor: !8fa724e8 (Heltec LoRa / Arduino Mega / DHT11)")
    print("-" * 68)
    print(f"{'Data / Hora (Brasília)':<22} | {'Temp (°C)':<10} | {'Umidade (%)':<12} | {'Rádio':<10}")
    print("-" * 68)

    temps = []
    umids = []

    for d in docs:
        quando = d.get("received_at") or d["_id"].generation_time
        # Converte para fuso local
        hora_str = quando.astimezone().strftime("%d/%m/%Y %H:%M:%S")
        payload = d.get("payload_data", {}).get("payload", {})
        sender = d.get("payload_data", {}).get("sender", "!8fa724e8")

        temp = payload.get("temp", payload.get("t"))
        umid = payload.get("umid", payload.get("u"))

        if temp is not None and umid is not None:
            temps.append(temp)
            umids.append(umid)
            print(f"{hora_str:<22} | {temp:>8.1f} °C | {umid:>10.1f} % | {sender:<10}")

    if temps:
        print("-" * 68)
        print("ESTATÍSTICAS DO INTERVALO:")
        print(f"  • Temperatura  ->  Média: {sum(temps)/len(temps):.2f} °C | Mín: {min(temps):.1f} °C | Máx: {max(temps):.1f} °C")
        print(f"  • Umidade Rel. ->  Média: {sum(umids)/len(umids):.2f} %  | Mín: {min(umids):.1f} % | Máx: {max(umids):.1f} %")
    print("=" * 68)

if __name__ == "__main__":
    formatar_relatorio()
