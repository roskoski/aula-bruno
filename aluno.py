import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. CRIAR O ARQUIVO CSV (Simulando a etapa de dados)
def criar_csv_exemplo():
    dados = {
        'Aluno': ['Ana', 'Ana', 'Ana', 'Bruno', 'Bruno', 'Bruno', 'Caio', 'Caio', 'Caio'],
        'Disciplina': ['Matematica', 'Portugues', 'Historia', 'Matematica', 'Portugues', 'Historia', 'Matematica', 'Portugues', 'Historia'],
        'N1': [8.5, 6.0, 4.0, 5.0, 9.0, 7.5, 3.0, 5.5, 6.0],
        'N2': [7.0, 5.5, 3.0, 4.5, 8.5, 8.0, 4.0, 6.0, 5.0]
    }
    df = pd.DataFrame(dados)
    df.to_csv('boletim.csv', index=False)
    print("-> Arquivo 'boletim.csv' criado com sucesso.")

# 2. PROCESSAMENTO DOS DADOS
def processar_boletim():
    # Ler o arquivo
    df = pd.read_csv('boletim.csv')
    
    # Calcular média por disciplina
    df['Media'] = df[['N1', 'N2']].mean(axis=1)
    
    # Definir Situação
    def checar_situacao(media):
        if media >= 7: return 'Aprovado'
        elif media >= 5: return 'Recuperação'
        else: return 'Reprovado'
    
    df['Situacao'] = df['Media'].apply(checar_situacao)
    return df

# 3. INTERFACE E GRÁFICOS
def sistema_principal():
    if not os.path.exists('boletim.csv'):
        criar_csv_exemplo()
    
    df = processar_boletim()
    
    while True:
        print("\n=== SISTEMA DE GESTÃO ESCOLAR ===")
        print("1. Listar Todos os Alunos")
        print("2. Filtrar Aluno e Gerar Gráficos")
        print("3. Estatísticas Gerais")
        print("4. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            print("\n", df.to_string(index=False))

        elif opcao == '2':
            print(f"\nAlunos disponíveis: {df['Aluno'].unique()}")
            nome = input("Digite o nome do aluno: ").strip()
            aluno_df = df[df['Aluno'].str.lower() == nome.lower()]

            if not aluno_df.empty:
                print(f"\nResultados para: {nome.capitalize()}")
                print(aluno_df[['Disciplina', 'Media', 'Situacao']].to_string(index=False))
                
                # Plotagem
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                
                # Gráfico de Barras (Médias)
                ax1.bar(aluno_df['Disciplina'], aluno_df['Media'], color='teal')
                ax1.axhline(y=7, color='red', linestyle='--', label='Corte')
                ax1.set_title(f'Médias de {nome.capitalize()}')
                ax1.set_ylim(0, 10)
                
                # Gráfico de Pizza (Situação das matérias)
                status_count = aluno_