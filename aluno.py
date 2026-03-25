import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Criar o arquivo CSV de exemplo (Etapa de preparação)
def criar_csv_exemplo():
    dados = {
        'Aluno': ['Ana', 'Ana', 'Ana', 'Bruno', 'Bruno', 'Bruno', 'Carlos', 'Carlos', 'Carlos'],
        'Disciplina': ['Matematica', 'Portugues', 'Historia', 'Matematica', 'Portugues', 'Historia', 'Matematica', 'Portugues', 'Historia'],
        'Nota1': [8.5, 6.0, 4.0, 5.0, 9.0, 7.0, 10.0, 8.0, 9.0],
        'Nota2': [7.0, 5.5, 3.0, 4.5, 8.5, 6.5, 9.5, 7.5, 8.5],
        'Nota3': [9.0, 6.5, 5.0, 6.0, 10.0, 8.0, 9.0, 8.5, 9.5]
    }
    df = pd.DataFrame(dados)
    df.to_csv('boletim.csv', index=False)
    print("Arquivo 'boletim.csv' criado/verificado com sucesso!")

# 2. Processar os dados e calcular médias e situações
def processar_boletim(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo)
    
    # Calcular média das 3 notas
    df['Media'] = df[['Nota1', 'Nota2', 'Nota3']].mean(axis=1).round(1)
    
    # Definir a situação
    def checar_situacao(media):
        if media >= 7: return 'Aprovado'
        elif media >= 5: return 'Recuperação'
        else: return 'Reprovado'
    
    df['Situacao'] = df['Media'].apply(checar_situacao)
    return df

# 3. Gerar gráficos
def exibir_graficos(df_aluno, nome_aluno):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Gráfico de Barras (Médias)
    ax1.bar(df_aluno['Disciplina'], df_aluno['Media'], color='teal')
    ax1.axhline(y=7, color='red', linestyle='--', label='Corte (7.0)')
    ax1.set_title(f'Médias por Matéria: {nome_aluno}')
    ax1.set_ylim(0, 10)
    ax1.legend()

    # Gráfico de Pizza (Situação)
    status = df_aluno['Situacao'].value_counts()
    ax2.pie(status, labels=status.index, autopct='%1.1f%%', colors=['#4CAF50', '#FFC107', '#F44336'])
    ax2.set_title('Distribuição de Desempenho')

    plt.tight_layout()
    plt.show()

# 4. Menu e Fluxo Principal
def sistema_principal():
    if not os.path.exists('boletim.csv'):
        criar_csv_exemplo()
    
    df = processar_boletim('boletim.csv')

    while True:
        print("\n" + "="*30)
        print("SISTEMA DE ANÁLISE ESCOLAR")
        print("="*30)
        print("1. Listar Boletim Geral")
        print("2. Analisar Aluno Específico (com Gráficos)")
        print("3. Ver Estatísticas da Turma")
        print("4. Sair")
        
        escolha = input("\nSelecione uma opção: ")

        if escolha == '1':
            print("\n", df[['Aluno', 'Disciplina', 'Media', 'Situacao']])
        
        elif escolha == '2':
            print(f"\nAlunos: {df['Aluno'].unique()}")
            nome = input("Digite o nome do aluno: ").strip()
            aluno_df = df[df['Aluno'].str.lower() == nome.lower()]
            
            if not aluno_df.empty:
                print("\n", aluno_df[['Disciplina', 'Media', 'Situacao']])
                exibir_graficos(aluno_df, nome.capitalize())
            else:
                print("\n[Erro] Aluno não encontrado.")

        elif escolha == '3':
            media_geral = df['Media'].mean()
            print(f"\n--- ESTATÍSTICAS ---")
            print(f"Média Geral de todos os alunos: {media_geral:.2f}")
            print(f"Total de matérias aprovadas: {len(df[df['Situacao'] == 'Aprovado'])}")
            print(f"Matéria mais difícil (menor média): {df.groupby('Disciplina')['Media'].mean().idxmin()}")

        elif escolha == '4':
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    sistema_principal()