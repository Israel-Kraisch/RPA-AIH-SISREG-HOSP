# Dicionário de Dados - Modelo Hospitalar para uso da AUTOMAÇÃO RPA com SISREG  
(Atualizado em 14/01/2026 – Joinville/SC)

Cada campo é apresentado com:

- **Nome do Campo**  
- Descrição detalhada  
- Tipo de dado esperado  
- Obrigatório no SISREG?  
- Regras / Validações oficiais do SISREG (com referências quando aplicável)

Os campos seguem a ordem exata das colunas no arquivo Excel modelo (`modelo_hospital_data_do_lote.xlsx` – aba "LOTE").

**cd_laudo**  
Código interno do laudo ou solicitação médica que originou o pedido de internação.  
**Tipo de dado**: Numérico ou string.  
**Obrigatório no SISREG?**: Não.  
**Regras / Validações oficiais do SISREG**: Não validado diretamente, mas essencial para rastreabilidade e auditoria clínica posterior (Portaria GM/MS nº 1.559/2008).

**dt_solicitacao**  
Data em que a internação foi solicitada.  
**Tipo de dado**: Data (DD/MM/YYYY).  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Para urgência: até 48h após internação. Para eletiva: data deve ser anterior ou igual à data prevista de internação (Portaria GM/MS nº 1.559/2008).

**tipo_atendimento**  
Classificação do tipo de atendimento que originou a solicitação.  
**Tipo de dado**: String (ex.: "Urgência / Internação / Ambulatorial").  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Define o fluxo regulatório. Ambulatorial pode exigir internação posterior; urgência permite autorização posterior (Portaria GM/MS nº 1.559/2008).

**nu_consulta**  
Número da consulta ambulatorial prévia registrada no SIGS.  
**Tipo de dado**: Numérico.  
**Obrigatório no SISREG?**: Sim para internações eletivas.  
**Regras / Validações oficiais do SISREG**: Vincula a justificativa clínica. Obrigatório para procedimentos eletivos não urgentes; sistema verifica existência no SIGS.

**auditado**  
Status interno do processamento do registro pelo RPA.  
**Tipo de dado**: Numérico inteiro (0 = pendente, 1 = processando, 2 = erro, 3 = sucesso, 4 = duplicado).  
**Obrigatório no SISREG?**: Não (campo exclusivo do RPA).  
**Regras / Validações oficiais do SISREG**: Não aplica (campo customizado). Serve para controle interno; no SISREG oficial, o status da AIH é controlado pelo sistema (ex.: pendente, autorizada, glosada).

**nu_internacao**  
Número da AIH (Autorização de Internação Hospitalar) gerada.  
**Tipo de dado**: Numérico (9 dígitos).  
**Obrigatório no SISREG?**: Não (gerado pelo sistema).  
**Regras / Validações oficiais do SISREG**: Gerado automaticamente após aprovação. Único e rastreável para faturamento SIH; duplicidade bloqueia nova solicitação.

**ds_motivo**  
Motivo do erro ou rejeição detectado pelo RPA.  
**Tipo de dado**: String.  
**Obrigatório no SISREG?**: Não (campo interno).  
**Regras / Validações oficiais do SISREG**: Não aplica. Útil para depuração e correção de lotes; no SISREG, motivos de rejeição são exibidos em alertas.

**estab_solicitante**  
Nome do estabelecimento que está solicitando a internação.  
**Tipo de dado**: String.  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Vinculado ao usuário logado e ao CNES solicitante. Deve ter permissão para solicitar AIH.

**cnes_sol**  
Código CNES do estabelecimento solicitante.  
**Tipo de dado**: Numérico (7 dígitos).  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Vinculado ao perfil do usuário. Deve ter permissão de regulador ou solicitante hospitalar (verificação automática).

**estab_executante**  
Nome do hospital ou unidade que realizará a internação.  
**Tipo de dado**: String.  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Deve corresponder exatamente ao CNES executor. Sistema valida habilitação e disponibilidade de leito.

**cnes_exe**  
Código CNES do estabelecimento executor.  
**Tipo de dado**: Numérico (7 dígitos).  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Deve estar habilitado no SIGTAP para o procedimento. Bloqueio se não habilitado ou sem vagas reguladas.

**nm_paciente**  
Nome completo do paciente.  
**Tipo de dado**: String.  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Deve coincidir com o nome registrado no CNS. Sistema verifica duplicidade de nomes + CNS.

**prontuario**  
Número do prontuário físico ou eletrônico do paciente no hospital.  
**Tipo de dado**: Numérico ou string.  
**Obrigatório no SISREG?**: Não.  
**Regras / Validações oficiais do SISREG**: Não validado, mas essencial para integração com sistemas locais.

**atendimento**  
Número interno do atendimento no sistema hospitalar.  
**Tipo de dado**: Numérico ou string.  
**Obrigatório no SISREG?**: Não.  
**Regras / Validações oficiais do SISREG**: Recomendado para rastreabilidade e evitar duplicidade local.

**nr_cns**  
Número do Cartão Nacional de Saúde do paciente.  
**Tipo de dado**: Numérico (15 dígitos).  
**Obrigatório no SISREG?**: Sim (prioridade máxima).  
**Regras / Validações oficiais do SISREG**: Deve passar no checksum, estar ativo e sem registro de óbito (integração com SIM). Bloqueio imediato se inválido ou duplicado (RNDS).

**dt_nascimento**  
Data de nascimento do paciente.  
**Tipo de dado**: Data (DD/MM/YYYY).  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Calcula idade automaticamente. Verifica compatibilidade com procedimento (ex.: pediátrico, geriátrico, obstétrico) – SIGTAP.

**tp_sexo**  
Sexo biológico ou declarado do paciente.  
**Tipo de dado**: String (M ou F).  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Valida compatibilidade com procedimentos (ex.: ginecológicos/obstétricos só para F). Incompatibilidade gera rejeição.

**tp_cor**  
Cor/raça declarada pelo paciente (conforme classificação SUS).  
**Tipo de dado**: String ou código SUS.  
**Obrigatório no SISREG?**: Não.  
**Regras / Validações oficiais do SISREG**: Opcional. Usado em relatórios de equidade racial no SUS.

**etnia**  
Etnia declarada pelo paciente (ex.: indígena, branca, preta, etc.).  
**Tipo de dado**: String ou código.  
**Obrigatório no SISREG?**: Não.  
**Regras / Validações oficiais do SISREG**: Opcional. Relevante para políticas de saúde indígena e relatórios de equidade.

**nm_mae**  
Nome completo da mãe do paciente.  
**Tipo de dado**: String.  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Usado para validação de identidade (cruzamento com RNDS/CNS). Essencial para evitar duplicidade de registros.

**telefone_contato**  
Número de telefone para contato com paciente ou responsável.  
**Tipo de dado**: String (ex.: "47 999999999").  
**Obrigatório no SISREG?**: Recomendado.  
**Regras / Validações oficiais do SISREG**: Não bloqueia, mas é usado para comunicação regulatória e confirmação de vagas.

**responsavel**  
Nome do responsável legal pelo paciente (geralmente para menores ou incapazes).  
**Tipo de dado**: String.  
**Obrigatório no SISREG?**: Sim para menores de idade.  
**Regras / Validações oficiais do SISREG**: Obrigatório quando paciente < 18 anos ou incapaz. Usado em notificações e consentimentos.

**ds_endereco**  
Endereço completo do paciente (rua, avenida, etc.).  
**Tipo de dado**: String.  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Parte da validação de residência. Deve ser compatível com CEP, bairro e município informados.

**nr_endereco**  
Número do imóvel (casa, apartamento, etc.).  
**Tipo de dado**: Numérico ou string.  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Complementa o endereço completo. Não validado isoladamente, mas necessário para completude.

**nm_bairro**  
Nome do bairro de residência do paciente.  
**Tipo de dado**: String.  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Deve ser compatível com CEP e município. Parte da verificação de residência.

**nm_cidade**  
Nome do município de residência.  
**Tipo de dado**: String.  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Deve coincidir com o código IBGE. Bloqueio se fora da área de regulação da central (pactuação CIR).

**cd_ibge**  
Código IBGE do município de residência do paciente.  
**Tipo de dado**: Numérico inteiro (6 ou 7 dígitos, ex.: 421010 para Mafra-SC).  
**Obrigatório no SISREG?**: Sim (indiretamente via validação de residência).  
**Regras / Validações oficiais do SISREG**: Verifica se o município está na área de abrangência da central reguladora ou se existe pactuação formal (CIR - Comissão Intergestores Regional).

**cd_uf**  
Sigla da Unidade Federativa (estado) de residência do paciente.  
**Tipo de dado**: String (2 caracteres maiúsculos, ex.: "SC").  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Deve coincidir com a UF da central reguladora ou existir acordo interestadual. Bloqueio automático se fora da jurisdição.

**nr_cep**  
Código de Endereçamento Postal (CEP) do paciente.  
**Tipo de dado**: Numérico (8 dígitos).  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Validação automática de endereço. Incompatível com município/UF gera erro ou rejeição.

**ds_sinais_sint_clinicos**  
Descrição dos sinais e sintomas clínicos apresentados pelo paciente.  
**Tipo de dado**: String (texto livre).  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Base clínica da solicitação. Deve ser detalhada e coerente com CID e procedimento. Auditoria pode glosar se genérica ou insuficiente.

**ds_cond_just_internacao**  
Texto que descreve a condição clínica que justifica a necessidade de internação.  
**Tipo de dado**: String (texto livre, até limite do campo).  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Deve ser claro, objetivo e suficiente para justificar a internação. Usado em auditorias clínicas e pode gerar glosa se insuficiente ou genérico (Portaria SAS/MS).

**ds_result_prov_diag**  
Resultados das provas diagnósticas realizadas que suportam o diagnóstico.  
**Tipo de dado**: String (texto livre).  
**Obrigatório no SISREG?**: Sim (especialmente em casos complexos).  
**Regras / Validações oficiais do SISREG**: Comprova o diagnóstico e a necessidade de internação. Obrigatório para justificar procedimentos invasivos ou de alta complexidade.

**ds_diagnostico**  
Descrição textual do diagnóstico (complementa o CID).  
**Tipo de dado**: String.  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Deve ser coerente com o CID informado. Auditoria manual pode glosar se houver discrepância ou falta de detalhe.

**cd_cid_principal**  
Código CID-10 do diagnóstico principal que justifica a internação.  
**Tipo de dado**: String (código CID-10 de 3 a 4 caracteres, ex.: "R91").  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Obrigatório para toda AIH. Deve ser compatível com o procedimento solicitado (regras automáticas do SIGTAP). Sistema valida também compatibilidade com idade e sexo do paciente. Incompatibilidade gera rejeição imediata após “Checar”.

**cd_cid_secundario**  
Código CID-10 do diagnóstico secundário (comorbidade ou complicação).  
**Tipo de dado**: String (código CID-10).  
**Obrigatório no SISREG?**: Não.  
**Regras / Validações oficiais do SISREG**: Similar ao principal: deve ser válido. Quando informado, contribui para o cálculo de complexidade e valor da AIH.

**cd_cid_causas_associadas**  
Código(s) CID-10 das causas associadas ao diagnóstico principal.  
**Tipo de dado**: String (código CID-10, pode conter múltiplos).  
**Obrigatório no SISREG?**: Não (opcional).  
**Regras / Validações oficiais do SISREG**: Deve ser código válido da CID-10. Quando informado, aumenta a complexidade da AIH e pode impactar a remuneração (grupos de procedimentos). Sistema verifica validade, mas não rejeita por ausência.

**proc_solicitado**  
Descrição textual do procedimento solicitado.  
**Tipo de dado**: String.  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Deve coincidir com o código SIGTAP. Usado em auditorias para validar a solicitação.

**cod_proc_solicitado**  
Código oficial do procedimento no SIGTAP.  
**Tipo de dado**: Numérico (exatamente 10 dígitos).  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Deve iniciar com "04" para internações. Verificado após "Checar". Incompatível com CID, idade, sexo ou habilitação do CNES gera rejeição automática (SIGTAP).

**clinica**  
Especialidade clínica ou tipo de leito solicitado.  
**Tipo de dado**: String (ex.: "CLINICA MEDICA").  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Deve ser compatível com o procedimento solicitado (validação SIGTAP). O sistema apresenta apenas opções habilitadas para o CNES executor.

**cd_carater_atendimento**  
Código que define o caráter da internação.  
**Tipo de dado**: Numérico inteiro (ex.: 1 = Eletiva, 2 = Urgência).  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Deve seguir tabela SUS (1=Eletiva, 2=Urgência). Para eletiva, exige autorização prévia; urgência permite posterior em até 48 horas (Portaria GM/MS nº 1.559/2008). Sistema bloqueia se incompatível com o tipo de procedimento ou situação clínica informada.

**documento**  
Tipo de documento de identificação do paciente.  
**Tipo de dado**: String (ex.: "CNS").  
**Obrigatório no SISREG?**: Sim (se CNS não informado).  
**Regras / Validações oficiais do SISREG**: Prioriza CNS; alternativos como RG/CPF só em casos excepcionais e com justificativa.

**nr_documento**  
Número do documento alternativo.  
**Tipo de dado**: String.  
**Obrigatório no SISREG?**: Não (se CNS presente).  
**Regras / Validações oficiais do SISREG**: Usado apenas quando CNS não está disponível. Menos priorizado que CNS.

**solicitante**  
Nome completo do profissional de saúde que solicitou a internação.  
**Tipo de dado**: String.  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Deve estar cadastrado no sistema com CPF e conselho válido. Sistema verifica vínculo profissional.

**cpf_solicitante**  
CPF do médico ou profissional que solicitou a internação.  
**Tipo de dado**: Numérico (11 dígitos).  
**Obrigatório no SISREG?**: Sim (se médico não cadastrado por CPF).  
**Regras / Validações oficiais do SISREG**: Deve ser válido e cadastrado no conselho profissional (CFM/CRM). Sistema verifica vínculo.

**nr_conselho**  
Número do registro no conselho profissional do solicitante.  
**Tipo de dado**: Numérico ou string.  
**Obrigatório no SISREG?**: Sim.  
**Regras / Validações oficiais do SISREG**: Verifica se o profissional está ativo no conselho (ex.: CFM) e compatível com o CBO.

**data_execucao**  
Data em que o RPA processou o registro.  
**Tipo de dado**: Data (DD/MM/YY).  
**Obrigatório no SISREG?**: Não (campo interno do RPA).  
**Regras / Validações oficiais do SISREG**: Não aplica; usado para log e auditoria do processo automatizado.

**hora_execucao**  
Hora exata em que o RPA concluiu o processamento.  
**Tipo de dado**: Hora (HH:MM:SS).  
**Obrigatório no SISREG?**: Não (campo interno do RPA).  
**Regras / Validações oficiais do SISREG**: Não aplica; útil para rastrear tempo de processamento.

**ds_concat**  
Justificativa concatenada enviada ao SISREG (combina consulta + condição).  
**Tipo de dado**: String (texto livre).  
**Obrigatório no SISREG?**: Sim (para o RPA, que alimenta o campo de justificativa).  
**Regras / Validações oficiais do SISREG**: Campo interno que alimenta o campo de justificativa no SISREG. Deve ser detalhado para evitar glosas em auditorias.
