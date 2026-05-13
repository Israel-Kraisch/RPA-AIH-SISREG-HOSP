# **Plano de Projeto de Desenvolvimento de Software: Robô de Digitação Automática no Sistema Sisreg para Inclusão de Fichas de Autorização de Internação Hospitalar \- AIH (RPA-AIH-SISREG)**

## **1\. Introdução**

O presente documento serve como norte para o projeto de desenvolvimento de software destinado à automação da digitação de fichas de Autorização de Internação Hospitalar (AIH) no Sistema Sisreg, ambiente onde é realizada a regulação e a fila de pacientes para internação e execução de procedimentos cirúrgicos, nos hospitais de média e alta complexidade, além de clínicas e policlínicas autorizadas  a realizar tais procedimentos conveniados ao SUS (Sistema Único de Saúde).

A **Solicitação de Autorização de Internação Hospitalar (AIH)** é um documento essencial no Sistema Único de Saúde (SUS) do Brasil. Sua finalidade é regulamentar e registrar a entrada de internação de pacientes em hospitais, assegurando o cumprimento de normas administrativas e legais.

### **Por que é necessário enviar a AIH em arquivo físico, e assinada para a Secretaria de Saúde?**

1. **Controle e Auditoria**: A AIH é utilizada para monitorar e comprovar a necessidade e a realização do atendimento hospitalar, evitando fraudes e garantindo o uso adequado dos recursos públicos.  
2. **Planejamento e Financiamento**: A Secretaria de Saúde utiliza os dados contidos nas AIHs para organizar o planejamento do sistema de saúde, como a alocação de recursos e a avaliação dos serviços prestados.  
3. **Registro Legal**: A AIH assinada é um documento que comprova a autorização da internação por um profissional médico, assegurando a legitimidade do processo.  
4. **Segurança Jurídica**: A assinatura do médico responsável atesta que a internação é clinicamente indicada, protegendo o paciente, o hospital e o próprio sistema público de saúde.

### **Leis e Normas que Estabelecem a Necessidade de Assinatura da AIH**

A exigência de assinatura e apresentação da AIH está fundamentada em diversas regulamentações:

1. [**LEI Nº 8.080/1990**](https://www.planalto.gov.br/ccivil_03/leis/l8080.htm): Estabelece os princípios do SUS, incluindo a garantia de acesso universal e regulamenta os mecanismos de controle e avaliação da assistência à saúde.  
   * **Art. 15, Inciso II**: Determina a organização do sistema de saúde, incluindo a regulação das internações hospitalares.  
2. [**DECRETO Nº 1.651/1995**](https://www.planalto.gov.br/ccivil_03/decreto/1995/d1651.htm): Regulamenta a operacionalização do SIH/SUS (Sistema de Informações Hospitalares do SUS), estabelecendo a obrigatoriedade da emissão da AIH para o controle das internações.  
3. [**PORTARIA SAS/MS Nº 692/2001**](https://bvsms.saude.gov.br/bvs/saudelegis/gm/2018/prt0692_26_03_2018.html): Detalha os procedimentos administrativos e técnicos relativos à emissão e utilização da AIH no âmbito do SUS.  
   * Exige que a AIH seja assinada por um médico responsável, comprovando a indicação clínica para internação.  
4. [**PORTARIA GM/MS Nº 1559/2008**](https://bibliotecadigital.economia.gov.br/bitstream/123456789/934/1/Pol%C3%ADtica%20Nacional%20de%20Regula%C3%A7%C3%A3o%20do%20Sistema%20%C3%9Anico%20de%20Sa%C3%BAde%20-%20SUS.docx): Regulamenta o uso do Cadastro Nacional de Estabelecimentos de Saúde (CNES) e reforça a importância da documentação adequada para auditoria e financiamento no SUS.  
5. **Normas Éticas do Conselho Federal de Medicina (CFM)**: De acordo com o Código de Ética Médica, o médico é responsável por atestar a necessidade de tratamentos ou internações com base em critérios técnicos e científicos.  
   

### **Necessidade de Apresentar a AIH Durante a Internação**

A apresentação da AIH é necessária para:

* Formalizar o registro administrativo da internação hospitalar.  
* Garantir que os custos do atendimento sejam corretamente registrados e posteriormente pagos pelo sistema público.  
* Possibilitar a realização de auditorias médicas e administrativas.  
* Facilitar o acompanhamento do tratamento do paciente pelo hospital e pela Secretaria de Saúde.

A AIH, portanto, não é apenas um requisito burocrático, mas um instrumento essencial para o funcionamento transparente e eficiente do sistema de saúde pública no Brasil.

##### 

### **Assinatura Digital e Digitalização de AIH**

A legislação brasileira tem avançado para permitir a digitalização dos processos de internação hospitalar, incluindo a Autorização de Internação Hospitalar (AIH).

A [**Lei nº 13.787, de 27 de dezembro de 2018**](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13787.htm), dispõe sobre a digitalização e a utilização de sistemas informatizados para a guarda, o armazenamento e o manuseio de prontuários de pacientes.

Essa lei estabelece que os prontuários podem ser digitalizados, desde que sejam asseguradas a integridade, autenticidade e confidencialidade dos documentos digitais.

Além disso, a [**Lei nº 14.063, de 23 de setembro de 2020**](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/lei/l14063.htm), trata sobre o uso de assinaturas eletrônicas em interações com entes públicos, incluindo a área da saúde.

Essa lei permite que documentos como receituários de medicamentos sujeitos a controle especial e atestados médicos sejam emitidos em meio eletrônico, desde que atendam aos requisitos estabelecidos pelo Ministério da Saúde.

Especificamente sobre a AIH, a partir de 1º de agosto de 2024,  conforme a [PORTARIA GM/MS/ Nº 4.477, DE 21 DE JUNHO DE 2024](https://www.in.gov.br/en/web/dou/-/portaria-gm/ms/-n-4.477-de-21-de-junho-de-2024-570280814) os laudos em formato digital deverão ser assinados eletronicamente, visando agilizar e simplificar o processo de autorização de internação hospitalar e procedimentos ambulatoriais.

É importante destacar que, ao implementar processos digitais, devem ser observadas as diretrizes da [**Lei Geral de Proteção de Dados Pessoais (LGPD)**](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm), Lei nº 13.709, de 14 de agosto de 2018, que estabelece normas para o tratamento de dados pessoais, garantindo a privacidade e a proteção das informações dos pacientes.

Portanto, a legislação atual permite e incentiva a digitalização dos processos de internação hospitalar, incluindo a AIH, desde que sejam cumpridos os requisitos legais para assegurar a segurança, autenticidade e confidencialidade das informações dos pacientes.

 Este projeto visa otimizar e agilizar o processo de inclusão de informações extraídas e obtidas dos diversos sistemas hospitalares, clínicas e policlínicas, que atualmente são AIH’s  impressas em papéis e que periodicamente são  encaminhadas a Secretaria Municipal de Saúde, objetivando auditoria, processamento por ordem de chegada e inclusão das informações de maneira manual, ou seja um operador lê e digita uma a uma, após a digitalização dos documentos impressos e transformados por OCR (Conversão para texto por captura de imagem).

Ocorre que a OCR manual e posterior a impressão, de um arquivo em papel, pode apresentar falhas de captura, e impedir a extração do texto de modo que seja viável a operação de cópia dos dados, seja por um operador humano, ou por uma automação, visto que os dados deverão ser buscado para a cópia e alimentação do sistema Sisreg.

Em ambos os casos, o preenchimento das informações no sistema fim poderia apresentar incorreções, falhas de preenchimento, ou ainda dados incompletos, seja por falha humana ou por dados de OCR incorretos, o que poderia impactar negativamente, causando demora na operação de preenchimento, obrigando o operador a realizar conferências acerca do preenchimento, e atrasar ou até mesmo impedir o tratamento de um paciente em aguardo pelo procedimento constante desta AIH.

Sugere-se portanto para o sucesso deste projeto,  que se alinhe, e estabeleça uma rotina com os hospitais, clínicas e policlínicas, onde, além de periodicamente, encaminharem as AIH’s em papel, encaminhem também um arquivo digital, em texto, com a estrutura de dados conforme o leiaute de AIH do MS, em um repositório central a ser disponibilizado pela Secretaria Municipal de Saúde de Joinville.

Não obstante, será imprescindível e  necessário que os hospitais, clínicas e policlínicas que estão sob o território da cidade de Joinville, (mesmo sob instâncias estaduais) conforme determina os atos regulamentares municipais vigentes ([Lei nº 9.219, de 12 de julho de 2022](https://sei.joinville.sc.gov.br/sei/publicacoes/controlador_publicacoes.php?acao=publicacao_visualizar&id_documento=10000014859677&id_orgao_publicacao=0), [Portaria nº 212/2023/SES](https://sei.joinville.sc.gov.br/sei/publicacoes/controlador_publicacoes.php?acao=publicacao_visualizar&id_documento=10000019991552&id_orgao_publicacao=0))   enviem ao município a partir de seus sistemas além das AIH impressas em papéis já encaminhados (devido a portarias do MS que exigem a assinatura do médico na AIH) os dados de cada AIH expressos em conteúdo de texto, tabular (CSV) ~~e ainda em PDF com o conteúdo disponível~~ para  cópia e extração, para que haja a importação de dados a partir destes arquivos e o preenchimento dos dados em uma AIH via automação no sistema Sisreg.

Caso haja a atualização ou migração de sistema no ministério da saúde, deverá ser realizado novo projeto para a adequação do modelo de dados e do robô RPA-AIH-SISREG.

## **2\. Objetivo**

O objetivo principal deste projeto é criar um robô para digitação automática (RPA-AIH-SISREG) que busque em um diretório central as informações de AIH encaminhadas pelos hospitais, clínicas e policlínicas, leia estes dados das diversas origens, e após o login por operador humano devidamente autorizado e com permissões no módulo Hospitalar para solicitações,  registre as mesmas no sistema Sisreg, minimizando a necessidade de entrada manual de dados para a Autorização de Internação Hospitalar. A automação visa garantir maior eficiência, redução de erros e economia de tempo para os usuários do sistema.

## **3\. Metas**

As metas específicas do projeto incluem:

* Desenvolvimento de um robô capaz de extrair dados de arquivos de Texto, CSV e formatos compatíveis de planilha (XLS, XLSX), tratar estes dados, e inseri-los em uma solicitação de AIH no sistema SISREG  
  * Optou-se ao longo do desenvolvimento por padronizar em XLSX.  
* Integração eficiente com o site Sisreg para inserção automática de informações.  
* Garantia da segurança e confidencialidade dos dados durante o processo de automação.  
* Implementação de funcionalidades de verificação e validação para garantir a precisão dos dados importados.  
* Treinamento e suporte aos operadores do robô para a utilização efetiva da ferramenta.

## **4\. Escopo**

O escopo do projeto abrange:

* Análise e identificação dos fluxos de trabalho e requisitos do sistema.  
* Desenvolvimento do RPA-AIH-SISREG.  
* Capacitação aos Analistas da área de Tecnologia da Informação da Secretaria Municipal da Saúde (Desenvolvimento e Inovação) nas ferramentas onde a solução será desenvolvida para suporte, manutenção e evolução após a entrega.   
* Integração com o site Sisreg.  
* Testes para garantir a funcionalidade e confiabilidade do software.

## **5\. Entregáveis**

Os principais entregáveis do projeto incluem:

* Software RPA-AIH-SISREG e CONVERSOR compilado em versão final estável.  
* Repositório de Arquivos com versionamento \- Sugere-se o Gitlab/Github  
* Todo o Código fonte versionado  
* Documentação técnica e manual do usuário.  
* Relatórios de testes e validação.

## **6\. Stakeholders**

Os principais stakeholders deste projeto são:

* Equipe de Tecnologia da Informação da SMS-JLLE (Secretaria Municipal de Saúde de Joinville)  
* Operadores do sistema Sisreg \- Unidades de Regulação da SMS-JLLE  
* Administradores dos sistemas hospitalares, clínicas e policlínicas.  
* Equipe de suporte técnico.

## **7\. Critérios de Sucesso**

O sucesso do projeto será avaliado com base nos seguintes critérios:

* Redução significativa no tempo de entrada de dados no sistema Sisreg  
  * Média de inclusão do registro de forma manual pelo operador humano 00:02:30 (dois minutos e trinta segundos) \- Dados coletados em gravação de inclusão por operador.  
    * Nota: Alguns casos levam até 15 minutos, principalmente onde há a necessidade de pesquisa prévia de consultas de origem.  
  * Estimativa média de inclusão por RPA 00:00:10 (dez segundos) \- Cerca de 15 vezes mais rápido que o operador humano.  
    * Nota: Toda a auditoria, pesquisas prévias de consulta devem ser realizadas antes de aplicar a automação, selecionando os registros para a inserção pelo RPA.  
* Precisão e consistência dos dados importados.  
* Aceitação positiva por parte dos usuários finais.  
* Implementação dentro dos prazos estabelecidos..

## **8\. Plano de Execução**

### **8.1 Atividades**

O desenvolvimento do projeto será dividido em fases distintas, cada uma composta por atividades específicas. As principais atividades incluem:

1. Levantamento de Requisitos:  
   * Identificação das necessidades dos usuários.  
   * Documentação dos requisitos do sistema.  
2. Desenvolvimento do Software:  
   * Implementação do RPA-AIH-SISREG.  
   * Integração com o site Sisreg.  
3. Testes e Validação:  
   * Realização de testes unitários, de integração e de sistema.  
   * Validação da precisão dos dados importados.  
4. Documentação e Treinamento:  
   * Elaboração de manuais técnicos e do usuário.  
   * Treinamento da equipe de suporte e usuários finais.  
5. Implementação e Monitoramento:  
   * Lançamento oficial do software.  
   * Monitoramento pós-implementação para ajustes e suporte contínuo.

### **8.2 Cronograma**

O projeto seguirá o seguinte cronograma:

| Fase | Início | Término  |
| ----- | ----- | ----- |
| Levantamento de Requisitos | 01/11/2023 | 06/09/2024 |
| Desenvolvimento do Software | 09/09/2024 | 10/01/2025 |
| Testes e Validação | 10/01/2025 | 24/01/2025 |
| Documentação e Treinamento | 01/11/2023 | 30/01/2025 |
| Implementação e Monitoramento | 30/01/2025 | 15/02/2025 |

## **9\. Riscos e Mitigações**

Identificamos alguns riscos potenciais que podem impactar o sucesso do projeto. As estratégias de mitigação incluem:

| Risco | Probabilidade | Impacto | Mitigação |
| :---- | :---- | :---- | :---- |
| Atrasos no desenvolvimento | Média | Alto | Alocar recursos adicionais, revisar o cronograma regularmente.  |
| Falta de Recurso Humano (Analista /  Desenvolvedor / Tester) | Média | Alto | Alocar recursos adicionais, contratar novo recurso, capacitar analistas já no quadro interno. |
| Mudanças na interface do Sisreg Web / Mudança de Sistema pelo governo do estado ou federal | Alta | Alto | Monitoramento contínuo da interface e adaptação do software quando necessário. |
| Erros na extração de dados da fonte externa | Média | Médio | Validação rigorosa dos dados e tratamento de exceções. |
| Problemas de desempenho | Baixa | Médio | Otimização do código e utilização de recursos adequados. |

## **10\. Revisão e Atualização do Plano**

Este plano será revisado periodicamente para garantir sua relevância e eficácia. As atualizações serão comunicadas a todos os stakeholders.

---

## **11\. Comunicação e Gerenciamento de Mudanças**

### **11.1 Comunicação**

Para garantir uma comunicação eficiente durante todo o projeto, serão realizadas reuniões regulares de status e atualizações por meio de canais específicos tais como e-mail, reunião online com agendamento prévio. Em caso necessário serão realizadas reuniões presenciais. 

**11.2 Gerenciamento de Mudanças**

Entendemos que mudanças podem ocorrer ao longo do projeto. Qualquer modificação no escopo ou prazos será avaliada quanto ao seu impacto. Mudanças significativas serão submetidas à aprovação dos stakeholders relevantes antes da implementação.

## **12\. Encerramento do Projeto**

O encerramento do projeto ocorrerá após a implementação bem-sucedida do RPA-AIH-SISREG no ambiente de produção do Sisreg. Esta fase incluirá:

* Avaliação do sucesso do projeto em relação aos critérios estabelecidos.  
* Coleta de feedback dos usuários finais.  
* Preparação de um relatório final que destaque os resultados alcançados.

## **13\. Anexos**

Os seguintes documentos serão anexados a este plano para referência adicional:

* [Apresentação inicial do projeto](https://docs.google.com/presentation/d/1DmnZBCfEegM1ajteBZKDTeH5N22iDs2ww_5oht-qymA/edit?usp=sharing)  
* [Documento de Requisitos do Sistema.](https://docs.google.com/document/d/1vFgHCEPJyl0Z8ItNpnOQqIBDHW2m-_TYbBS7awTpFss/edit?usp=sharing)  
* [Manual de solicitações hospitalares no SISREG](https://www.saude.sc.gov.br/edocman/areas-de-atuacao/regulacao-sur/manuais/sisreg_solicitante_hospitalar.pdf)  
* [Wiki do Sistema SISREG III \- Como Solicitar Internação](https://wiki.saude.gov.br/SISREG/index.php/Categoria:SOLICITAR_INTERNA%C3%87%C3%83O)  
* [Wiki do Sistema SISREG III \- Manuais e Informações](https://wiki.saude.gov.br/SISREG/index.php/P%C3%A1gina_principal)  
* [Projeto no Gitlab](https://gitlab.joinville.sc.gov.br/ses/rpa-aih-sisreg)  
* [Ofício com solicitação de dados digitais](https://sei.joinville.sc.gov.br/sei/controlador.php?acao=procedimento_trabalhar&id_procedimento=10000026447440&id_documento=10000026447443)

## **14\. Aprovação do Plano**

Este plano é considerado aprovado pelos representantes abaixo descritos:

**Nome e Cargo do Responsável pelo Projeto:** \[Assinatura\] Data: \_\_\_\_\_\_\_

**Nome e Cargo do Patrocinador do Projeto:** \[Assinatura\] Data: \_\_\_\_\_\_\_

**Nome e Cargo do Gerente de Desenvolvimento:** \[Assinatura\] Data: \_\_\_\_\_\_\_

**Nome e Cargo do Gerente de Qualidade:** \[Assinatura\] Data: \_\_\_\_\_\_\_

**Nome e Cargo do Usuário Final Representante:** \[Assinatura\] Data: \_\_\_\_\_\_\_

---

Este plano servirá como guia durante todo o ciclo de vida do projeto, fornecendo diretrizes claras para a equipe e garantindo a entrega bem-sucedida do RPA-AIH-SISREG no ambiente do Sisreg.

## **15\. Gestão de Qualidade**

A gestão de qualidade é fundamental para o sucesso do projeto. Serão estabelecidos procedimentos e padrões para garantir a entrega de um produto de alta qualidade. Isso incluirá revisões de código, testes rigorosos e a aplicação de melhores práticas de desenvolvimento de software.

## **16\. Treinamento e Capacitação**

Um plano abrangente de treinamento será desenvolvido para capacitar a equipe de suporte técnico e os usuários finais na utilização eficiente do RPA-AIH-SISREG. Workshops e materiais didáticos serão elaborados para garantir uma transição suave para a nova solução.

## **17\. Sustentabilidade**

Considerações de sustentabilidade serão incorporadas ao projeto, visando a eficiência energética, a otimização de recursos e a minimização do impacto ambiental. Isso incluirá práticas de codificação eficientes e o uso responsável de recursos de hardware.

## **18\. Avaliação Pós-Implementação**

Após a implementação, uma fase de avaliação será conduzida para medir o desempenho real do RPA-AIH-SISREG em comparação com os objetivos estabelecidos. Feedback adicional dos usuários será coletado para identificar áreas de melhoria contínua.

## **19\. Considerações Finais**

Este plano detalhado proporciona uma estrutura sólida para o desenvolvimento, implementação e gestão contínua do projeto. A colaboração efetiva entre as partes interessadas, a atenção à qualidade e a gestão proativa de riscos são elementos críticos para o sucesso.

## **20\. Contatos**

Em caso de dúvidas, preocupações ou necessidade de informações adicionais, os seguintes contatos podem ser acionados:

* **Unidade de Regulação:** [Franci Maiara Machado](mailto:franci.machado@joinville.sc.gov.br) \- [franci.machado@joinville.sc.gov.br](mailto:franci.machado@joinville.sc.gov.br)   
* **Patrocinador do Projeto:**  [Silvio Lucenir Zietz](mailto:silvio.zietz@joinville.sc.gov.br) \- silvio.zietz@joinville.sc.gov.br   
* **Analistas de Desenvolvimento:** [Israel Kraisch](mailto:israel.kraisch@joinville.sc.gov.br) \- [israel.kraisch@joinville.sc.gov.br](mailto:israel.kraisch@joinville.sc.gov.br) [Ricardo Dias Lemos dos Santos](mailto:ricardo.dias@joinville.sc.gov.br) \- [ricardo.dias@joinville.sc.gov.br](mailto:ricardo.dias@joinville.sc.gov.br)   
* **Usuário Final Representante:** [Talita Maria Meris Poffo](mailto:\<talita.meris@joinville.sc.gov.br\>) \- [talita.meris@joinville.sc.gov.br](mailto:talita.meris@joinville.sc.gov.br)

## **21\. Plano de Ação**

Para a digitalização dos processos de Autorização de Internação Hospitalar (AIH), podemos seguir um plano de ação dividido em etapas, desde a análise dos processos atuais até a implementação da automação.

**Plano de Ação para Digitalização dos Processos de AIH**

#### **1\. Análise dos Processos Atuais**

* **Objetivo:** Compreender o fluxo de trabalho atual, identificar pontos críticos e mapear todos os processos manuais envolvidos na solicitação e aprovação de AIH.  
* **Ação:** Realizar reuniões com os envolvidos (equipe médica, administrativos e TI), levantar documentações e fluxos operacionais existentes.

#### **2\. Definição dos Requisitos**

* **Objetivo:** Especificar os requisitos funcionais e não funcionais do novo sistema digital.  
* **Ação:** Criar um documento de requisitos detalhado, incluindo funcionalidades essenciais, integrações necessárias e requisitos de segurança.

#### **3\. Digitalização dos Formulários e Documentos**

* **Objetivo:** Transformar todos os formulários e documentos de AIH para formatos digitais.  
* **Ação:**  
  * Abrir conversas e formalizar pedido de informações de AIH aos Hospitais conveniados ao Sus.   
    * ✅ HSJ \- Hospital Municipal São José \- Sistema: Soul MV \- Oracle **(Piloto \- Fase 1\)**  
    * ✅ Hospital Bethesda \- Sistema: Tasy **(Piloto \- Fase 1\)**  
    * 🚫 HJAF \- Hospital Infantil Dr. Jesser Amarante Faria \- Sistema: Tasy **(Fase 2\)**  
    * 🚫HRHDS \- Hospital Regional Hans Dieter Schimidt \- Sistema: Micromed **(Fase 3\)**  
    * 🚫Clinica Oftalmus \- Sistema Verificar **(Fase 3\)**  
    * 🚫HDH \- Hospital Dona Helena \- Sistema: Tasy **(Fase 2\)**  
    * 🚫CHU \- Centro Hospitalar Unimed Joinville  \- Sistema: Tasy **(Fase 2\)**  
  * Criar versões digitais dos formulários, exportar diretamente do software de origem, usar softwares para conversão, extrair os dados de bases de dados dos sistemas de origem, para inserção de dados.  
* 

#### **4\. Desenvolvimento da Automação (RPA)**

* **Objetivo:** Implementar a automação para a inserção e processamento de dados nos sistemas necessários.  
* **Ferramentas:** Utilizar Python com Selenium e WebDriver e ferramentas de software open source, capazes para automatizar tarefas repetitivas e suscetíveis a erros humanos.  
* **Ação:** Desenvolver scripts para:  
  * Extração e armazenamento dos dados do sistema hospitalar.   
    * O hospital de origem deve gerar o arquivo com base no leiaute indicado.  
  * A partir da extração gerar planilha (conversor) para auditoria e seleção dos dados para execução.  
  * Inserção automática dos dados de texto, csv  para o sistema SISREG.  
  * Verificação automática dos campos obrigatórios e envio dos dados para solicitação de internação hospitalar.

#### **5\. Testes e Validação**

* **Objetivo:** Garantir que o sistema automatizado funcione conforme o esperado.  
* **Ação:** Realizar testes de unidade, integração e sistema. Validar os resultados com casos de uso reais e ajustar o sistema conforme necessário.

#### **6\. Treinamento e Capacitação**

* **Objetivo:** Capacitar a equipe envolvida para utilizar o robô.  
* **Ação:** Conduzir sessões de treinamento, criar manuais de usuário e fornecer suporte inicial.

#### **7\. Implantação**

* **Objetivo:** Colocar o robô em produção.  
* **Ação:** Implementar a solução em um ambiente de produção, monitorar o desempenho e fornecer suporte inicial.

#### **8\. Monitoramento e Melhoria Contínua**

* **Objetivo:** Assegurar que o sistema continue operando de forma eficiente e eficaz.  
* **Ação:** Monitorar o sistema, corrigir bugs a partir de solicitações do operador e realizar melhorias contínuas com base no feedback dos usuários.

## **22\. Agradecimentos**

Agradecemos a todos os envolvidos no projeto pelo comprometimento e esforço dedicados. Juntos, estamos trabalhando para alcançar os objetivos estabelecidos e garantir o sucesso do RPA-AIH-SISREG no contexto do Sisreg.

---

Este documento está sujeito a revisões e atualizações conforme necessário.
