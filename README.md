# RPA-AIH-SISREG

<div align="center">
  <img src="RPA-AIH-SISREG/IMG/AIH-PRONT.jpg" alt="Logo do Projeto" width="20%"/>
  <br>
  <img src="https://img.shields.io/badge/Status-Ativo-brightgreen" alt="Status">
</div>

## Nome
RPA-AIH-SISREG

## Descrição

Robô de automação de processo de digitação, que inclui solicitaçoes de Autorização de Internação Hospitalar no sistema [SISREG](https://sisregiii.saude.gov.br/) encaminhadas pelos Hospitais conveniados que realizam procedimentos cirurgicos pelo SUS.

## Pré Requisitos
Verifique o arquivo de requirements

Programa conversor, que realiza a rotina antes manual, analisa os dados da AIH em arquivo csv,onde após a postagem dos arquivos em uma pasta temporaria, executa as atividades:

- Lista o diretorio dos arquivos de origem e lê e processa pela seguencia de postagem, todos os arquivos encaminhados, onde a cada arquivo recebido, realiza o processamento, analisa os dados, cria a estrutura de auditoria e processamento. 

- E gera no destino de execução do RPA o arquivo pronto para a inclusão das solicitações. 


Necessário ChromeDriver local compativel com os sistema operacional (x86 ou x64)
ou liberação de firewall / proxy para a conexão. 

Necessário adequar o fonte caso use o ChromeDriver local

Necessário usuário e senha de uso como operador de inclusão de solicitações no SISREG

### Arquivos na pasta

` * [Chromedriver.exe](https://developer.chrome.com/docs/chromedriver/downloads?hl=pt-br) = Trata-se de um intermediador entre o codigo .py e o browser GoogleChrome, para controle do mesmo. a versão dele deve sempre combinar com a versão do do browser, vide versão em "Configurações" ->  "Sobre".

* RPA-AIH-SISREG = Codigo para controle do browser e envio dos dados.

* RPA-AIH-SISREG/PADROES/aih_hospital_data_do_lote.csv = Arquivo modelo com os dados para envio, os dados são recebidos via e-mail ou repositorio de dados, dentro do modelo de tabulação desse arquivo pelo responsável de cada unidade hospitalar. -> Dados apenas de exemplo impersonificados. 


INSTALAÇÃO

* instalar o Python 3.12.4 - (sugere-se instalar o Anaconda Python) 

* copiar os arquivos dentro de uma pasta do diretorio

* atraves do prompt usar o comando ( python -m venv venv ) para criacao de um ambiente virtual

* em seguida /venv/script/activate.bat executar 

* pip install -r ./requirements.txt

* ainda no prompt para executar o conversor para tratamento dos dados com comando python ./conversor.py

* ainda no prompt para executar o robô usar o comando python ./RPA-AIH-SISREG.py`

* para compilar use PyInstaller e os hooks auxiliares.

## Support
Projeto criado e desenvolvido pelo [Núcleo de Tecnologia da Informação da Secretaria Municipal de Saúde de Joinville](mailto:ti.saude@joinville.sc.gov.br) - NTI-SES

## Roadmap

[x] - [Apresentação do Projeto](https://docs.google.com/presentation/d/1DmnZBCfEegM1ajteBZKDTeH5N22iDs2ww_5oht-qymA/edit?usp=sharing)

[x] - [Plano de Projeto de Implementação de Software](RPA-AIH-SISREG/DOCS/02_PPDS_RPA_AIH_SISREG.md)

[x] - [Análise de Requisitos e Documentação](RPA-AIH-SISREG/DOCS/03_Implementacao_de_Software_RPA_AIH_SISREG.md)

[X] - Desenvolvimento Fase 1 - Conversor e RPA

[X] - Testes de Carga

[x] - [Capacitação dos Stakeholders](RPA-AIH-SISREG/DOCS/04_Manual_do_Usuario.md) (Gerência da Unidade de Regulação)

[x] - Execução em Produção 13/01/2025

[x] - Desenvolvimento Fase 2 - Interface Grafica e Logs

[x] - Implantação em hospitais da rede estadual de SC

[x] - Acompanhamento de distribuição. 

[x] - Conclusão e entrega de codigo fonte a DTIG SC



## Autores
### Autores e contato

| Nome                          | Contato                              |
|-------------------------------|--------------------------------------|
| **[Israel Kraisch]**       | [israel.kraisch@joinville.sc.gov.br](mailto:israel.kraisch@joinville.sc.gov.br) |
| **[Ricardo Dias Lemos dos Santos**   | [ricardodiaslemos@yahoo.com.br](mailto:ricardodiaslemos@yahoo.com.br) |
| **[Franci Maiara Machado]**  | [franci.machado@joinville.sc.gov.br](mailto:franci.machado@joinville.sc.gov.br) |

### Como obter acesso ao código-fonte e aos artefatos
Este é um repositório privado.  
Se você deseja acessar o código-fonte, executáveis ou documentação:

1. Crie uma conta no GitHub (se ainda não tiver)  
2. Envie seu usuário do GitHub, e-mail e contato telefonico para **Israel Kraisch** por e-mail  
3. Nós adicionaremos você como colaborador após analise de pedido de acesso.

Depois de adicionado você terá acesso total ao repositório e às Releases (instaladores, manuais etc.).

### Licença
Este projeto está licenciado sob a **GNU Affero General Public License v3.0 (AGPL-3.0)**  
Isso significa que você pode:
- Usar livremente (pessoal ou comercial)
- Modificar e distribuir
- Mas qualquer versão modificada deve:
  - Ter o código-fonte publicado publicamente
  - Manter este aviso de copyright e créditos dos autores originais

Uso comercial permitido ✓ Modificações permitidas ✓ Distribuição permitida ✓  
Obrigatório publicar o código-fonte das versões modificadas e manter os créditos dos autores originais.

[Leia a licença completa aqui](LICENSE)

## Status
Liberado para uso

## Limitação de Responsabilidade por Modificações:
O software original é disponibilizado sem garantias de qualquer natureza. Caso o software seja modificado, alterado ou customizado por terceiros, a responsabilidade civil, técnica e penal pelo código modificado passará a ser exclusivamente de quem realizou as alterações. Os autores originais não assumem qualquer obrigação, suporte ou responsabilidade por danos diretos, indiretos ou incidentais decorrentes de versões modificadas do software."

**

## Notas desta versão 7.2

** Atenção - este software foi desenvolvido seguindo modelos e regras estabelecidas pelo SISREG, pela SUR/SC (Superintendencia de Regulação de SC) suas Centrais Regulatórias Regionais e NIR (Nucleos de Internação e Regulação).

 

Clinica Fixa - Envia todas as solicitações para a Fila de Cirurgia Geral. 

Validações Desabilitadas: O Que São e Por Que Foram Desabilitadas?

No código original, o script automatiza o preenchimento de solicitações de internação hospitalar (AIH - Autorização de Internação Hospitalar) no SISREG. Para isso, ele faz validações automáticas para garantir que o paciente atenda a certos critérios, como residência em um município específico (no caso, Joinville-SC) e tipo de moradia (ex.: não ser nômade, morador de rua ou cigano).

Essas validações eram feitas consultando o texto da página do SISREG após pesquisar o CNS (Cartão Nacional de Saúde) do paciente. Se o paciente não atendesse, o script marcava o registro como "erro" (auditado = 2) e adicionava um motivo no Excel.

Validações Específicas Desabilitadas:

Validação de Município de Residência: 

Verificava se o paciente mora em "JOINVILLE - SC". 
Isso era feito procurando no texto da página frases como "Município de Residência: JOINVILLE - SC".

Validação de Tipo de Moradia: 

Se o paciente fosse de Joinville, mas classificado como "NÔMADE", "CIGANO" ou "MORADOR DE RUA", 
o script rejeitava a solicitação, pois esses casos não têm residência fixa e podem não ser elegíveis para certos serviços locais.

Como Foram Desabilitadas no Código?

O código foi modificado para ignorar essas verificações, permitindo que o script prossiga mesmo se o paciente não atender a esses critérios. 

Isso é útil se:

Sua unidade de saúde quer processar solicitações de pacientes de outros municípios (ex.: referenciados).
Há uma política local para aceitar casos especiais (como moradores de rua).
Você quer evitar rejeições automáticas e revisar manualmente no SISREG.

Impactos:

Vantagens: O processo fica mais rápido e flexível. Você pode processar mais registros sem interrupções.

Riscos: Se o paciente não for elegível, o SISREG pode rejeitar a solicitação manualmente. 
Monitore os logs e o Excel para ver se há erros reais.

Como Reativar? 
Basta remover os comentários e testar! 
