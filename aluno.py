import pandas as pd
import matplotlib.pyplot as plt

def carregar_dados(caminho):
    try:
        df = pd.read_csv(caminho)
        return df
    except FileNotFoundError:
        print("Erro: Arquivo CSV não encontrado!")
        return None

def processar_notas(df):
    # Calcular a média das notas (Nota1, Nota2, Nota3)
    df['Media'] = df[['Nota1', 'Nota2', 'Nota3']].mean(axis=1).round(2)
    
    # Definir situação
    # Aprovado >= 7 | Recuperação >= 5 e < 7 | Reprovado < 5
    def definir_situacao(media):
        if media >= 7: return 'Aprovado'
        elif media >= 5: return 'Recuperação'
        else: return 'Reprovado'
    
    df['Situacao'] = df['Media'].apply(definir_situacao)
    return df

def gerar_graficos(df_aluno, nome_aluno):
    # Configuração da figura com dois subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Gráfico de Barras: Médias por Disciplina
    ax1.bar(df_aluno['Disciplina'], df_aluno['Media'], color='skyblue', edgecolor='navy')
    ax1.axhline(y=7, color='red', linestyle='--', label='Média Aprovação')
    ax1.set_title(f'Médias por Disciplina - {nome_aluno}')
    ax1.set_ylim(0, 10)
    ax1.legend()

    # Gráfico de Pizza: Distribuição de Situações
    contagem_situacao = df_aluno['Situacao'].value_counts()
    ax2.pie(contagem_situacao, labels=contagem_situacao.index, autopct='%1.1f%%', startangle=140, colors=['#66b3ff','#99ff99','#ff9999'])
    ax2.set_title('Status das Disciplinas')

    plt.tight_layout()
    plt.show()

def menu_principal():
    df = carregar_dados('notas_alunos.csv')
    if df is None: return

    df = processar_notas(df)

    while True:
        print("\n--- SISTEMA DE BOLETIM ESCOLAR ---")
        print("1. Ver todos os dados")
        print("2. Filtrar por Aluno e Gerar Gráficos")
        print("3. Estatísticas Gerais")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n", df.to_string(index=False))
        
        elif opcao == '2':
            alunos_disponiveis = df['Aluno'].unique()
            print(f"\nAlunos cadastrados: {', '.join(alunos_disponiveis)}")
            nome = input("Digite o nome do aluno: ")
            
            aluno_data = df[df['Aluno'].str.lower() == nome.lower()]
            
            if not aluno_data.empty:
                print("\n", aluno_data[['Disciplina', 'Media', 'Situacao']].to_string(index=False))
                gerar_graficos(aluno_data, nome.capitalize())
            else:
                print("Aluno não encontrado.")

        elif opcao == '3':
            print("\n--- ESTATÍSTICAS GERAIS ---")
            print(f"Média Geral da Turma: {df['Media'].mean():.2f}")
            print(f"Total de Aprovações: {len(df[df['Situacao'] == 'Aprovado'])}")
            print(f"Maior nota registrada: {df['Media'].max()}")

        elif opcao == '4':
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_principal()