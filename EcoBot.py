import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

BANCO_DE_DADOS = {
    frozenset(["Plástico", "Metal"]): [
        "Lata para armazenamento",
        "Robô de Brinquedo",
        "Suporte de celular"
    ],
    frozenset(["Plástico", "Papel"]): [
        "Papel de Parede",
        "Livro de Capa Plastificada",
        "Cartão com Blister"
    ],
    frozenset(["Plástico", "Vidro"]): [
        "Luminária de Vidro com Base de Plástico",
        "Garrafa Térmica",
        "Óculos de Proteção"
    ],
    frozenset(["Plástico", "Borracha"]): [
        "Tênis Esportivo",
        "Pneu de Carrinho de Controle Remoto",
        "Cabo de Ferramenta Emborrachado"
    ],
    frozenset(["Vidro", "Metal"]): [
        "Lâmpada Incandescente",
        "Espelho com Moldura Metálica",
        "Termômetro Antigo"
    ],
    frozenset(["Vidro", "Papel"]): [
        "Quadro com Proteção de Vidro",
        "Vitral com Molde de Papelão",
        "Frasco de Perfume com Rótulo"
    ],
    frozenset(["Vidro", "Borracha"]): [
        "Garrafa de Vidro com Rolha de Borracha",
        "Conta-gotas",
        "Ampola com Vedação de Borracha"
    ],
    frozenset(["Metal", "Papel"]): [
        "Clipe de Papel com Revestimento",
        "Caderno de Espiral Metálica",
        "Etiqueta Metálica em Caixa"
    ],
    frozenset(["Metal", "Borracha"]): [
        "Lápis com Borracha e Anel Metálico",
        "Selo Mecânico",
        "Válvula de Pneu"
    ],
    frozenset(["Papel", "Borracha"]): [
        "Carimbo com Cabo de Papel Prensa",
        "Envelope com Tira Emborrachada",
        "Bloco Autoadesivo (Post-it)"
    ]
}

MATERIAIS_DISPONIVEIS = ["Plástico", "Vidro", "Metal", "Papel", "Borracha"]


# 3. Interface Visual com Menu de Seleção Dropdown (Discord Select Menu)
class SelectMateriaisView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60) # O menu expira em 60 segundos
        
        # Cria a lista de opções para o usuário escolher
        options = [
            discord.SelectOption(label=mat, description=f"Selecionar {mat}") 
            for mat in MATERIAIS_DISPONIVEIS
        ]
        
        # Select que permite escolher no mínimo 2 e no máximo 2 opções
        self.select = discord.ui.Select(
            placeholder="Escolha exatamente 2 materiais recicláveis...",
            min_values=2,
            max_values=2,
            options=options
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        # Pega as 2 escolhas do usuário
        escolhas = self.select.values
        chave = frozenset(escolhas)
        
        # Busca no dicionário
        itens = BANCO_DE_DADOS.get(chave, [])
        
        if itens:
            resposta = (
                f"♻️ **Materiais Selecionados:** {escolhas[0]} e {escolhas[1]}\n\n"
                f"🔍 **3 Itens criados a partir desses dois materiais:**\n"
                f"1. {itens[0]}\n"
                f"2. {itens[1]}\n"
                f"3. {itens[2]}"
            )
        else:
            resposta = "Não foram encontrados itens para essa combinação."

        # Responde o usuário
        await interaction.response.send_message(resposta, ephemeral=True)


# 4. Comando Slash no Discord (/reciclar)
@bot.tree.command(name="reciclar", description="Escolha 2 materiais para ver itens feitos com eles.")
async def reciclar(interaction: discord.Interaction):
    view = SelectMateriaisView()
    await interaction.response.send_message(
        "Selecione **2 materiais recicláveis** na lista abaixo:", 
        view=view, 
        ephemeral=True
    )


# 5. Evento de Inicialização
@bot.event
async def on_ready():
    # Sincroniza os comandos Slash com o Discord
    await bot.tree.sync()
    print(f"Bot online como {bot.user}")

bot.run("TOKEN_AQUI")





