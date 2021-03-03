# Decisões que foram tomadas

* Estratégia de Branching
    Adotada a estratégia Trunk-Based visando simplificar o processo e também garantir segurança (via política de Pull Request), onde os merges das branches adjacentes são realizadas para a branch main (trunk) e a partir dela é inciado o fluxo de CICD da aplicação.

* Containerization
    Para viabilizar os testes locais, garantir maior velocidade na preparação de ambiente de execução da aplicação e possibilitar maior portabilidade, foi realizado o containerization da aplicação.
    No processo de desenvolvimento foi realizado um refactoring no Dockerfile, redefinindo a imagem base de Python para Alpine

* Plataforma de Orquestração de Pipelines: Azure Pipelines
    Escolhido o Azure Pipelines pela paridade com o Github, alta diversidade de Tasks (reduzindo o tempo de escrita de scripts) e pelo alto nível de integração com serviços externos a serem consumidos (DockerHub e Azure Portal)
    Como estratégia, foi adotado o Multi-stage Pipeline e utilizada a abordagem de "Pipeline as Code", versinando a definição do Pipeline como arquivo yml no repositório da aplicação.
    Também foi utilizado a feature Library para armazenar as variáveis e secrets em Variable Group.

* Estratégia de Build
    Geração de artefato da imagem Docker e push no DockerHub, possibilitando o teste e consumo em vários tipos de ambientes (Azure Container Instance, Azure WebApps for Containers, K8s, etc)

* Estratégia de Deploy
    Infra as Code escrito em ARM Templates para provisionamento e configuração de ambiente Azure (ACI).
    Escolhido o Azure Container Instance por ser um serviço direcionado à execução de containers que suporta o Pull da imagem (DockerHub ou Azure Container Registry) diretamente no provisionamento do recurso.

* Monitoramento e métricas
    Escolhido Azure Application Insights por ser uma ferramenta robusta que entrega a Telemetria (logs e métricas) da aplicação e com a simplicidade de configuração no código via SDK.



# Arquiteturas que foram testadas e motivos de modifica-las/abandona-las

* Azure WebApp for Containers
    Testada implantação para o serviço, mas ocorreu problemas com o map das portas do container para o host.

* Azure Container Registry como Repositório de Imagens Docker
    Modificada para DockerHub, devido à complexidade de provisionamento e consumo no IaC do recurso Azure Container Registry.


# Testes executados

* Testes locais para conteinerização
* Testes locais de execução e consumo da API
* Testes com publicação de imagem no DockerHub
* Testes com provisionamento do recurso Container Instance no Azure


# Ideias para implementar se tivesse tempo

> Pipeline
>> Normalizar os templates de CI/CD para entrega do tipo de aplicação
>> Implementação de testes para validação de código Python (Lint), configurando as dependências e os scripts para teste

> Taggeamento de imagem Docker
>> Aplicar tags conforme ambiente e versão de publicação

> Melhoria em Monitoria
>> Criação de eventos de notificação com disparo de alertas conforme métricas ofensoras da aplicação
>> Criação de Dashboards para otimizar a visualização