import os
import pandas as pd
import json
import PyPDF2
from pathlib import Path

MAPA_FICHEIROS = {
    # PDFs
    "horario.pdf": "Horário semanal das aulas do aluno, com dias da semana, horas, salas e disciplinas.",
    "ImprimirConsultaNotas.pdf": "Pauta oficial de notas curriculares, disciplinas realizadas, classificações finais e ECTS.",
    "matricula_inscricao_1.pdf": "Comprovativo oficial de matrícula e inscrição - Parte 1.",
    "matricula_inscricao_2.pdf": "Comprovativo oficial de matrícula e inscrição - Parte 2.",
    "matricula_inscricao_3.pdf": "Comprovativo oficial de matrícula e inscrição - Parte 3.",

    # CSVs úteis
    "data (1).xlsx": "Inscrições em exames (Melhorias, Época Normal/Recurso).",
    "data (2).xlsx": "Resumo estatístico de créditos ECTS inscritos por ano letivo.",
    "data (4).xlsx": "Plano Curricular Completo: Notas finais, disciplinas aprovadas/inscritas e ano curricular.",
    "data (5).xlsx": "Histórico de turmas onde o aluno esteve inscrito.",
    "data (6).xlsx": "Média do curso atual e ponderada.",
    "data (7).xlsx": "Lista de Unidades Curriculares (Cadeiras) oferecidas no curso.",
    "data (8).xlsx": "Performance anual: ECTS aprovados e média por ano.",
    "data (12).xlsx": "Regras de validação do ciclo de estudos (créditos obrigatórios vs opcionais).",
    "data (15).xlsx": "Registo de assiduidade e aulas dadas.",
    "data (19).xlsx": "Histórico de requisições e pedidos académicos.",
    "data (23).xlsx": "Extrato de Conta Corrente: Faturas, notas de crédito e documentos financeiros.",
    "data (24).xlsx": "Detalhes de Propinas e pagamentos a regularizar.",
}

def processar_extras_2_0():
    pasta_raiz = Path(__file__).parent.parent
    pasta_uploads = pasta_raiz / "dados_netpa" / "downloads_2.0"
    
    arquivo_destino = pasta_raiz / "files_reading" / "json_ficheiros_2.0.json"

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
                        t = pagina.extract_text()
                        if t: texto_extraido += t + "\n"
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
        print(f"Erro ao salvar JSON: {e}")

if __name__ == "__main__":
    processar_extras_2_0()