### **Manual do Usuário   \- Automação de Inserção de Dados de AIH no SISREG**

Versão 1 \- 27/01/2025  
---

#### **Introdução**

Este manual descreve como utilizar o software de automação para extração e inserção de dados de solicitação de Autorização de Internação Hospitalar (AIH) no Sistema de Regulação (SISREG).

---

#### **Requisitos do Sistema**

* **Hardware mínimo:**  
  * Memória RAM: 8GB  
  * Processador: 4 núcleos  
  * Internet estável  
  * Navegador Google Chrome (e Chrome Driver compatível)

---

#### **Configuração Inicial**

Certifique-se de que o diretório principal do aplicativo está configurado conforme a estrutura abaixo:

`RPA-AIH-SISREG/`  
`├── LOTES/`  
`├── config/`  
`├── CONVERSOR-AIH.exe`  
`├── RPA-AIH-SISREG.EXE`  
`├── aih_hosp_lote_data.csv`

---

#### **Fluxograma do Processo**

**Etapas do Processo:**

1. Recepção do arquivo CSV \-\> Verifique o e-mail, e baixe para a pasta raiz da aplicação  
2. Conversão para XLSX \-\> execute o conversor e verifique o arquivo gerado  
3. Auditoria dos dados \-\> faça as correções necessárias e marque as linhas para execução  
4. Processamento no SISREG \-\> Execute o RPA e aguarde a finalização  
5. Revisão de logs e relatórios. \-\> Revise o arquivo e tome as ações necessárias.

#### **Fluxo de Uso**

1. **Realizar baixa de arquivo**  
   * Baixe o arquivo original do Hospital (`aih_hosp_lote_data.csv)`, a partir do e-mail corporativo, e salve na pasta RPA-AIH-SISREG  
2. **Processar Arquivos AIH**  
   * Execute o programa `CONVERSOR-AIH.exe` para converter os dados do lote no formato Excel (.xlsx).  
   * O arquivo tratado será salvo no diretório **LOTES**, e o original será movido para **LOTES/bkp**.  
3. **Auditar Dados**  
   * Abra o arquivo gerado no diretório **LOTES** em um editor de planilhas.  
   * Note que a coluna “nu consulta” traz a informação marcada como “0” (zero) isto indica que a linha não será processada.   
     1. Mantenha o registro com zero, se não localizar a solicitação física em papel, neste caso a linha não será processada.  
   * Verifique no SIGS pesquisando pelo nome do usuário de uma AIH a processar, listada no arquivo e presente no lote físico (solicitação em papel) uma consulta que originou o pedido de AIH.  
   * Preencha a coluna “nu consulta” com o número da consulta localizada para o paciente.  
   * Preencha a coluna "auditado" com o numeral `1` para indicar que a linha está pronta para processamento.  
   * Salve o arquivo no mesmo diretório e não altere a extensão ou seja o arquivo deve manter o nome e a extensão (exemplo aih\_hsj\_lote\_data.xlsx)  
4. **Inserir Dados no SISREG**  
   * Execute o programa `RPA-AIH-SISREG.exe`  
   * Insira seu login e senha quando solicitado.  
   * O sistema processará as linhas auditadas e registrará os resultados no arquivo.  
5. **Verificar Logs e Relatórios**  
   * Após a finalização, acesse o arquivo novamente e verifique a coluna “auditado” para consultar os registros do processo:  
     1. se houver linhas com o numeral 3 marcado, o registro da solicitação da AIH foi concluído  
     2. se houver linhas com o numeral 4 marcado, indica que já existe  registro da solicitação da AIH presente no sisreg, tome as medidas necessárias para o atendimento do paciente.  
     3. se houver linhas com o numeral 2 marcado, verifique a coluna de erros “ds\_motivo” para identificar o que ocorreu:  
        1. caso seja possível ajuste a informação e remarque com o numeral 1 na coluna “auditado” para reprocessamento.  
        2. caso seja apresentado um erro técnico  (geralmente escrito em inglês) tente re-executar o registro remarque com o numeral 1 na coluna “auditado” para reprocessamento.  
- Caso ainda assim o registro não seja processado, solicite a análise da equipe de ti para a correção do programa, abrindo um chamado e adicionando o conteúdo da linha para análise.

#### **Mensagens de Status**

* **Processamento Bem-Sucedido:**  
  * A linha foi processada e a AIH foi incluída no SISREG. O status da coluna **auditado** será atualizado para `3`.  
* **Erro no Processamento:**  
  * Caso o sistema encontre um erro (ex.: falta de informações obrigatórias), a coluna **auditado** será marcada como `2` e detalhes do problema estarão em **ds\_motivo**.  
* **Revisão Necessária:**  
  * Quando o sistema identifica uma AIH já existente para o paciente, o status será marcado como `4`, indicando que o operador deve revisar o registro.

#### **Regras de Operação**

1. **Preparação dos Arquivos**  
   * Certifique-se de que os arquivos no formato CSV enviados pelos hospitais estão corretamente salvos no diretório raiz da aplicação.   
   * Garanta que os nomes dos arquivos seguem o padrão `aih_hosp_lote_data.csv`  
2. **Conversão e Tratamento de Dados**  
   * O arquivo será convertido para o formato XLSX com as colunas adicionais de controle:  
     * **nu\_consulta**: Número da consulta que originou o atendimento.  
     * **auditado**: Indicador para processamento (0 \= não auditado, 1 \= pronto para lançamento, 2 \= erro revisão necessária, 3 \= processado, 4 \= preexiste aih, revisão necessária).  
     * **nu\_internacao**: Número da internação gerado no SISREG após o processamento.  
     * **ds\_concat**: Justificativa para internação concatenada com o número da consulta.  
     * **ds\_motivo**: Relatório de erros ou informações adicionais.  
3. **Auditoria do Operador**  
   * Após o processamento inicial, abra o arquivo `aih_hosp_lote_data.XLSX` gerado no diretório **LOTES**.  
   * Preencha a coluna **auditado** com `1` para as linhas que devem ser processadas.  
   * Salve o arquivo após a auditoria.  
4. **Processamento Automático**  
   * Execute o programa `RPA-AIH-SISREG.exe`  
   * O sistema lerá as linhas marcadas como auditadas (`auditado = 1`) e fará a inserção dos dados no SISREG automaticamente.  
   * As colunas **nu\_internacao**, **ds\_motivo** e **auditado** serão atualizadas conforme o resultado do processamento.  
5. **Logs e Relatórios**  
   * Após a execução, um log detalhado será gerado no diretório **LOGS** contendo:  
     * Registros processados com sucesso.  
     * Erros encontrados.  
     * Estatísticas do processo.

---

#### **Resolução de Problemas**

1. **Erro na Conexão com o SISREG**  
   * Verifique sua conexão com a internet.  
   * Certifique-se de que as credenciais de login estão corretas.  
2. **Falha no Processamento de Linhas**  
   * Consulte a coluna "ds\_motivo" no arquivo auditado para entender a falha.  
   * Corrija as inconsistências e reprocesse o arquivo.

---

**Segurança e Conformidade**

1. **Proteção de Dados**  
   * Todos os arquivos contendo informações de pacientes devem ser armazenados em um local seguro e acessível apenas a usuários autorizados.  
   * Certifique-se de que os dados processados estejam em conformidade com a **Lei Geral de Proteção de Dados (LGPD)**.  
2. **Acesso Restrito**  
   * Apenas operadores devidamente autorizados e treinados devem acessar o sistema e os arquivos de AIH.  
   * As credenciais para login no SISREG devem ser mantidas em sigilo e nunca compartilhadas.  
3. **Manutenção de Logs**  
   * Os logs gerados pelo sistema devem ser revisados regularmente para garantir a rastreabilidade das operações.  
   * Em caso de auditoria, os registros devem ser apresentados como evidência do cumprimento dos processos definidos.

---

#### **Fluxo Completo de Operações**

1. **Recepção do Arquivo de AIH**  
   * O operador baixa os arquivos de AIH encaminhados por hospitais conveniados.  
   * Os arquivos são salvos no diretório RPA-AIH-SISREG  para processamento.  
2. **Conversão e Tratamento de Dados**  
   * O software **CONVERSOR-AIH.exe** é executado, gerando um arquivo no formato xlsx pronto para auditoria.  
   * O operador verifica a integridade e a consistência dos dados gerados.  
3. **Auditoria**  
   * O operador revisa os registros, preenche a coluna **auditado** e insere o número da consulta (**nu\_consulta**)  
4. **Automação da Inserção no SISREG**  
   * O programa  **RPA-AIH-SISREG** é executado, e as linhas auditadas são inseridas no sistema.  
   * Erros ou exceções são registrados automaticamente no arquivo e no log.  
5. **Relatórios e Logs**  
   * Após o processamento, o operador acessa os relatórios para verificar o status das inserções.  
   * Logs detalhados são analisados para corrigir possíveis inconsistências.

#### **Suporte Técnico**

Caso encontre problemas não previstos, entre em contato com o suporte técnico responsável pelo sistema, fornecendo as seguintes informações:

* Nome do arquivo processado.  
* Log do processamento (disponível no diretório **LOGS**).  
* Capturas de tela, se aplicável.

##### Contato para Suporte Técnico

Caso precise de assistência adicional, entre em contato com a equipe de suporte técnico:

**Central de Serviços \- [Formulário para solicitar ajuda](https://glpi10.pmjlle.joinville.sc.gov.br/plugins/formcreator/front/formdisplay.php?id=307)**

**Telefone:** 3481 5186 \- Ramal Interno 6013

**E-mail:** [ti.saude@joinville.sc.gov.br](mailto:ti.saude@joinville.sc.gov.br)

**Horário de Atendimento:** Segunda a Sexta, das 8h às 18h.

#### 

#### **Exemplos de Situações Comuns**

* **Erro no Formato do Arquivo CSV:**  
  Certifique-se de que o arquivo segue o padrão exigido. Caso contrário, revise o conteúdo ou solicite um novo envio ao hospital conveniado.  
* **Campos Obrigatórios em Branco:**  
  Revise o arquivo na etapa de auditoria e preencha os campos ausentes antes de iniciar o processamento.  
* **Conexão Interrompida Durante a Inserção:**  
  O sistema salva o progresso e permite reprocessar as linhas que não foram concluídas. Revise a conexão com a internet antes de tentar novamente.

---

#### **FAQs (Perguntas Frequentes)**

1. **O que fazer se o arquivo CSV não for reconhecido pelo sistema?**  
   * Verifique se o arquivo está no diretório correto e segue o padrão esperado.  
   * Renomeie o arquivo para `aih_hosp_lote_data.csv (onde hosp= nome do hospital, lote é o número de lote, e data a data do lote encaminhado)` e tente novamente.  
2. **Como lidar com erros registrados na coluna *ds\_motivo*?**  
   * Revise os detalhes do erro fornecido.  
   * Faça as correções necessárias no arquivo auditado e re-execute o processo.  
3. **O sistema não consegue fazer login no SISREG. O que pode estar errado?**  
   * Verifique suas credenciais de acesso.  
   * Certifique-se de que o navegador Chrome e o Chrome Driver estão atualizados.  
4. **Posso reprocessar um arquivo já tratado?**  
   * Sim, desde que ele esteja no formato correto e as colunas de controle sejam ajustadas conforme necessário.

#### **Plano de Contingência.**

1. **Falhas no Software**  
   * **Sintoma:** O sistema trava ou fecha inesperadamente.  
   * **Ação:**  
     * Reinicie o software.  
     * Verifique os logs para identificar possíveis erros.  
     * Certifique-se de que todas as dependências estão instaladas corretamente (verifique o arquivo `requirements.txt`).  
2. **Erro de Login no SISREG**  
   * **Sintoma:** O sistema não aceita as credenciais ou não conclui o login.  
   * **Ação:**  
     * Confirme que as credenciais estão corretas.  
     * Verifique se a conexão com a internet está estável.  
     * Atualize o Google Chrome e o Chrome Driver para a versão mais recente.  
3. **Perda de Dados Durante o Processamento**  
   * **Sintoma:** Dados processados não aparecem na planilha ou no log.  
   * **Ação:**  
     * Revise os logs para entender onde ocorreu o erro.  
     * Certifique-se de que o arquivo original não foi corrompido.  
     * Refaça o processamento utilizando um backup do arquivo original.  
4. **Mudanças no Sistema SISREG**  
   * **Sintoma:** O script falha ao navegar ou preencher dados no SISREG.  
   * **Ação:**  
     * Notifique imediatamente a equipe técnica responsável.  
     * Aguarde a manutenção e atualize o programa para refletir as alterações na interface do SISREG.

---

#### **Boas Práticas Operacionais**

#### **Dicas para Melhor Uso**

1. **Organização dos Arquivos**  
   * Mantenha os arquivos originais, tratados e logs organizados em suas respectivas pastas: **LOTES**, **bkp** e **LOGS**.  
   * Nomeie os arquivos de forma padronizada para facilitar a localização e o histórico de processamento.  
2. **Revisão Regular**  
   * Sempre revise os arquivos auditados antes de iniciar o processamento.  
   * Sempre revise o conteúdo da coluna **ds\_motivo** em busca de possíveis erros antes de reprocessar.  
   * Verifique a consistência dos dados, como formatos de datas e preenchimento de campos obrigatórios.  
3. **Testes Antes de Processar Grandes Volumes**  
   * Realize testes em pequenos lotes antes de executar em grandes volumes para garantir a precisão do processo.  
4. **Manutenção do Sistema**  
   * Certifique-se de que o sistema operacional e o navegador Chrome estão atualizados.

#### 

   

---

#### **Glossário**

* **AIH:** Autorização de Internação Hospitalar. Documento que permite a internação do paciente na rede hospitalar.  
* **SISREG:** Sistema de Regulação utilizado pelo Ministério da Saúde para gerenciar internações, consultas e outros serviços de saúde.  
* **RPA (Robotic Process Automation):** Tecnologia utilizada para automatizar tarefas repetitivas, como inserção de dados em sistemas.  
* **CSV:** Formato de arquivo (valores separados por vírgula) utilizado para troca de dados tabulares.

---

#### **Exemplos Práticos de Operação**

1. **Conversão de Arquivo AIH (CSV para XLSX)**  
   **Passos:**  
   * Abra o Windows Explorer  
   * Navegue até o diretório onde está o arquivo original `aih_hosp_lote_data.csv`  
   * Execute o programa `CONVERSOR-AIH.exe`  
   * Verifique no diretório **LOTES** o arquivo XLSX gerado com o nome `aih_hosp_lote_data.xlsx`.  
   * O arquivo original será movido para o diretório **LOTES/bkp**.  
2. **Resultados Esperados:**  
   * Um novo arquivo Excel pronto para auditoria.  
   * O arquivo conterá as colunas adicionais de controle (`nu_consulta`, `auditado`, `ds_motivo`, entre outras).

---

2. **Auditoria do Arquivo XLSX**  
   **Passos:**  
   * Abra o arquivo gerado (`aih_hosp_lote_data.xlsx`) no editor de planilhas.  
   * Insira os números das consultas na coluna **nu\_consulta**, conforme análise de auditoria.  
   * Atualize a coluna **auditado** para `1` nas linhas que estão prontas para processamento.  
   * Salve o arquivo e mantenha-o no diretório **LOTES**.  
3. **Resultados Esperados:**  
   * Colunas **nu\_consulta** e **auditado** devidamente preenchidas, indicando os registros prontos para inserção no SISREG.

---

3. **Processamento Automático com o RPA**  
   **Passos:**  
   * Execute o programa `RPA-AIH-SISREG.exe`  
   * O sistema solicitará suas credenciais de login no SISREG. Insira-as corretamente.  
   * Acompanhe a barra de progresso e as mensagens exibidas na interface.  
4. **Resultados Esperados:**  
   * Registros auditados serão inseridos automaticamente no SISREG.  
   * A coluna **nu\_internacao** será preenchida com o número da internação gerado.  
   * Logs detalhados serão armazenados no diretório **LOGS**.

---

4. **Revisão de Logs e Relatórios**  
   **Passos:**  
   * Após a execução do RPA, acesse o diretório **LOGS**.  
   * Verifique o arquivo de log mais recente para analisar o status de cada registro processado.  
   * Consulte o campo **ds\_motivo** no arquivo XLSX para identificar possíveis falhas ou erros.  
5. **Resultados Esperados:**  
   * Detalhamento completo dos registros processados, erros encontrados e ações necessárias.

---

#### **Cenários de Uso Comuns**

1. **Erro ao Executar o Conversor**  
   * **Causa:** Arquivo original CSV fora do padrão esperado.  
   * **Solução:**  
     * Abra o arquivo no Excel para verificar inconsistências.  
     * Ajuste os campos obrigatórios e salve novamente como CSV antes de reexecutar o conversor.  
     * Solicite novo arquivo do lote ao hospital.  
2. **Erro de Conexão Durante o Processamento**  
   * **Causa:** Instabilidade na internet ou queda do sistema SISREG.  
   * **Solução:**  
     * Verifique a conectividade da rede.  
     * Refaça o login e continue o processo de onde parou.  
3. **Registro Não Processado**  
   * **Causa:** Campo obrigatório ausente ou inconsistência nos dados.  
   * **Solução:**  
     * Revise o arquivo XLSX.  
     * Preencha os campos ausentes e reexecute o processo.

---

#### **Casos de Uso \- Exemplos Detalhados**

##### **Caso de Uso 1: Processar um Arquivo de AIH**

**Descrição:**  
Um operador precisa converter o arquivo CSV enviado pelo hospital conveniado para o formato XLSX, realizando o tratamento e adicionando colunas de controle.

**Passos:**

1. Certifique-se de que o arquivo CSV está no diretório **raiz junto do programa de conversão** e segue o padrão `aih_hosp_lote_data.csv`.  
2. Execute o programa `CONVERSOR-AIH.exe`  
3. Verifique se o arquivo `aih_hosp_lote_data.xlsx` foi gerado corretamente no diretório **LOTES**.  
4. Abra o arquivo no editor de planilhas para confirmar as colunas adicionadas:  
   * **nu\_consulta**: Inicialmente vazia.  
   * **auditado**: Preenchido com `0` para todos os registros.  
   * **ds\_motivo**: Inicialmente vazia.

**Resultado Esperado:**  
O arquivo `aih_hosp_lote_data.xlsx` estará disponível para auditoria, e o original será armazenado em **LOTES/bkp/**`aih_hosp_lote_data.csv`.

---

##### **Caso de Uso 2: Auditoria de Registros**

**Descrição:**  
O operador precisa revisar e atualizar os dados no arquivo XLSX para garantir que os registros estão prontos para processamento.

**Passos:**

1. Abra o arquivo `aih_hosp_lote_data.xlsx` no editor de planilhas.  
2. Verifique cada registro, preenchendo as colunas:  
   * **nu\_consulta**: Insira o número da consulta relacionado ao atendimento.  
   * **auditado**: Atualize para `1` os registros prontos para inserção no SISREG.  
3. Salve o arquivo no mesmo diretório **LOTES** e com a mesma extensão do arquivo.

**Resultado Esperado:**  
Os registros prontos para processamento estarão marcados com `1` na coluna **auditado**.

---

##### **Caso de Uso 3: Inserção no SISREG**

**Descrição:**  
Após a auditoria, o operador utiliza o RPA para inserir os registros no sistema SISREG.

**Passos:**

1. Execute o programa `RPA-AIH-SISREG.exe`  
2. Insira suas credenciais de login no SISREG quando solicitado.  
3. O sistema processará as linhas marcadas como **nu\_consulta** que estiverem preenchidas e com **auditado \= 1**  no arquivo XLSX.  
4. Durante o processamento:  
   * As colunas **nu\_internacao** e **ds\_motivo** e **auditado** serão atualizadas conforme o status de cada registro.  
   * Logs serão gerados e salvos no diretório **LOGS**.

**Resultado Esperado:**

* Registros processados com sucesso terão a coluna **auditado** atualizada para `3`.  
* Registros com erros terão a coluna **auditado** atualizada para `2` e terão detalhes preenchidos em **ds\_motivo**.  
* Registros processados cujo se encontre pré-existente de AIH terão a coluna **auditado** atualizada para `4` e terão detalhes preenchidos em **ds\_motivo**.

---

#### **Estatísticas de Processamento**

Ao final de cada execução, o sistema lançará uma tela com o relatório com os seguintes dados:

* Total de registros processados.  
* Total de registros com sucesso.  
* Total de erros identificados.  
* Tempo total de execução.

O relatório estará disponível no log correspondente e poderá ser compartilhado via webhook corporativo, se configurado.

---

#### **Conclusão**

Este manual foi criado para fornecer todas as informações necessárias para que os operadores utilizem o sistema de automação de maneira eficaz, garantindo eficiência, segurança e conformidade com as normas, e foi projetado para facilitar o uso do sistema de automação de inserção de dados no SISREG. 

Ao seguir as instruções, você garantirá a precisão e a eficiência do processo, minimizando erros e otimizando o fluxo de trabalho.

O uso adequado do sistema reduzirá significativamente o tempo de processamento e os erros associados à inserção manual de AIHs no SISREG.

Caso precise de treinamento adicional, atualizações no sistema ou personalizações neste documento, entre em contato com o suporte técnico ou a equipe de TI responsável.

