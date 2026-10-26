"""
Gera automaticamente uma imagem PNG estilizada como terminal (dark mode)
contendo as leituras reais de temperatura e umidade salvas no MongoDB.
Arquivo gerado: print_leituras.png
"""
import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
import matplotlib.pyplot as plt

load_dotenv()

def gerar_imagem_print():
    client = MongoClient(os.environ["MONGO_URI"])
    col = client[os.environ["MONGO_DB"]][os.environ["MONGO_COLLECTION"]]

    filtro = {
        "payload_data.sender": "!8fa724e8",
        "payload_data.payload.t": {"$exists": True}
    }

    docs = list(col.find(filtro).sort("_id", -1).limit(12))[::-1]

    # Prepara o texto do terminal
    linhas = [
        "PS C:\\Users\\felip\\GitHubAllan> python relatorio_leituras.py",
        "=" * 66,
        "      FATEC SHUNJI NISHIMURA - PROJETO INTEGRADOR VI (BIG DATA)",
        "        MONITORAMENTO IOT / MESHTASTIC + MONGODB (DHT11)",
        "=" * 66,
        f"Coleção: iot.sensores | Total de registros: {col.estimated_document_count()}",
        "Rádio emissor: !8fa724e8 (Heltec LoRa / Arduino Mega / DHT11)",
        "-" * 66,
        f"{'Data / Hora (Brasília)':<22} | {'Temp (°C)':<10} | {'Umidade (%)':<12} | {'Rádio':<8}",
        "-" * 66
    ]

    temps, umids = [], []
    for d in docs:
        quando = d.get("received_at") or d["_id"].generation_time
        hora_str = quando.astimezone().strftime("%d/%m/%Y %H:%M:%S")
        p = d.get("payload_data", {}).get("payload", {})
        temp = p.get("temp", p.get("t"))
        umid = p.get("umid", p.get("u"))
        if temp is not None and umid is not None:
            temps.append(temp)
            umids.append(umid)
            linhas.append(f"{hora_str:<22} | {temp:>8.1f} °C | {umid:>10.1f} % | !8fa724e8")

    if temps:
        linhas.append("-" * 66)
        linhas.append("ESTATÍSTICAS DO INTERVALO:")
        linhas.append(f"  • Temperatura  -> Média: {sum(temps)/len(temps):.1f} °C | Mín: {min(temps):.1f} °C | Máx: {max(temps):.1f} °C")
        linhas.append(f"  • Umidade Rel. -> Média: {sum(umids)/len(umids):.1f} %  | Mín: {min(umids):.1f} % | Máx: {max(umids):.1f} %")
    linhas.append("=" * 66)

    texto_completo = "\n".join(linhas)

    # Criação da imagem estilizada (Terminal VS Code Dark)
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=150)
    fig.patch.set_facecolor('#1e1e1e')
    ax.set_facecolor('#1e1e1e')

    # Remove eixos
    ax.axis('off')

    # Desenha o texto com fonte monospace
    ax.text(
        0.04, 0.95, texto_completo,
        transform=ax.transAxes,
        fontsize=9.5,
        fontfamily='monospace',
        verticalalignment='top',
        color='#4ec9b0',
        bbox=dict(boxstyle='square,pad=0.8', facecolor='#181818', edgecolor='#333333', lw=1.5)
    )

    caminho_img = os.path.join(os.path.dirname(__file__), "print_leituras.png")
    plt.tight_layout()
    plt.savefig(caminho_img, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()

    print(f"\n[SUCESSO] Imagem do print gerada com sucesso em: {caminho_img}\n")

if __name__ == "__main__":
    gerar_imagem_print()
