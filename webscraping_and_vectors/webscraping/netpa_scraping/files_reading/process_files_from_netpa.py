import os
import pandas as pd
import json
import PyPDF2
from pathlib import Path

MAPA_FICHEIROS = {
    # PDFs
    "horário.pdf": "Horário semanal das aulas do aluno, com dias, horas, disciplinas e salas.",
    "ImprimirConsultaNotas.pdf": "Pauta oficial de notas curriculares, disciplinas, classificações e créditos ECTS.",
    "matricula_inscricao_1.pdf": "Comprovativo de matrícula e inscrição do aluno - Parte 1.",
    "matricula_inscricao_2.pdf": "Comprovativo de matrícula e inscrição do aluno - Parte 2.",
    "matricula_inscricao_3.pdf": "Comprovativo de matrícula e inscrição do aluno - Parte 3.",

    # CSVs úteis
    "data (1).xlsx": "Inscrições em épocas de exame (Melhorias, Época Normal).",
    "data (2).xlsx": "Resumo de créditos ECTS inscritos por ano letivo.",
    "data (4).xlsx": "Plano Curricular detalhado: notas finais, situação (Aprovado/Inscrito) e ano curricular.",
    "data (5).xlsx": "Histórico de turmas do aluno por ano letivo.",
    "data (6).xlsx": "Média do aluno por ano curricular.",
    "data (7).xlsx": "Lista completa de unidades curriculares (cadeiras) do curso por semestre.",
    "data (8).xlsx": "Resumo de ECTS aprovados e média ponderada por ano.",
    "data (12).xlsx": "Regras de validação do ciclo de estudos (créditos obrigatórios).",
    "data (15).xlsx": "Detalhes de assiduidade ou horas das UCs.",
    "data (19).xlsx": "Pedidos académicos (requisições) e datas.",
    "data (23).xlsx": "Extrato de conta corrente (Faturas, Pagamentos e Propinas).",
}

def processar_extras():
    pasta_raiz = Path(__file__).parent.parent
    pasta_uploads = pasta_raiz / "dados_netpa" / "downloads"

    arquivo_destino = pasta_raiz / "files_reading" / "json_ficheiros.json"

    novos_dados = []

    if not pasta_uploads.exists():
        print(f"Erro: A pasta '{pasta_uploads}' não existe.")
        return

    for ficheiro, descricao in MAPA_FICHEIROS.items():
        caminho_completo = pasta_uploads / ficheiro

        texto_extraido = ""

        # Ler PDF
        if str(caminho_completo).lower().endswith(".pdf"):
            try:
                with open(caminho_completo, 'rb') as f:
                    leitor = PyPDF2.PdfReader(f)
                    for pagina in leitor.pages:
                        texto_extraido += pagina.extract_text() + "\n"
            except Exception as e:
                print(f"Erro PDF {ficheiro}: {e}")

        # Ler Excel
        elif "xlsx" in str(caminho_completo):
            try:
                df = pd.read_excel(caminho_completo)
                
                if not df.empty:
                    texto_extraido = df.to_string(index=False)
            except Exception as e:
                print(f"Erro Excel {ficheiro}: {e}")

        if texto_extraido:
            conteudo_final = f"FONTE: {descricao}\n\nCONTEÚDO:\n{texto_extraido}"
            novos_dados.append({
                "nome": ficheiro,
                "xpath": "",
                "conteudo": conteudo_final
            })
            print(f"Processado: {ficheiro}")

    try:
        os.makedirs(os.path.dirname(arquivo_destino), exist_ok=True)
        with open(arquivo_destino, 'w', encoding='utf-8') as f:
            json.dump(novos_dados, f, ensure_ascii=False, indent=4)
            
        print(f"Criado: {arquivo_destino}")

    except Exception as e:
        print(f"Erro ao salvar: {e}")

if __name__ == "__main__":
    processar_extras()