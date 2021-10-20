
Revolut - DevOps Engineer Test

Forewords

O job proposto contempla a criação de um conjunto de apis que poderia ser feito de maneira mais simpleficada. O que cairia como uma luva no momento que chegou. Certamente esta é a época do ano mais assoberbada, no entanto as palavras da recrutadora ficaram na minha cabeça: "faça uma coisa de que se orgulhe".

Mais uma vez dizer isso é uma decisão arriscada, pois sempre há a possibilidade de ser dito que este código não seja motivo de orgulho.

Então por que gastar um tempo que não tenho e ainda se expor desta forma?

Por que me permitiu endereçar issues que encontro em projetos reais. Por que me fez sair da zona e conforto da aws e do on premisse para explorar novas ferramentas. Enfim, abrir novos horizontes.

Arquitetura

O objetivo do código é dar a possibilidade ao desenvolvedor colocar diretamente seu código em produção garantindo que um conjunto de testes unitários seja executado. Além desses, aplicar análise de código estático que dentre outras coisas garante códigos de fácil manutenção e que os códigos sejam seguros (OWASP 10) .

Tecnologias envolvidas:

1) python 
2) Docker / DockerHub como registry / aws ec2
3) Sonaqube
4) mysql / aws ec2
5) github / Actions como cicd
6) mysql - aws, ec2, vpc, storage, security rules (iam & inbound/outbound)
7) Kubernetes - google cloud platform 

Clouds envolvidas

Como dito anteriormente, se fosse para manter a zona de conforto todo o deploy seria feito na aws, inclusive o cicd. Decedi manter os itens "comodities" como o banco de dados mysql e o sonarqube na aws. Isso consumiu 45 min de trabalho e permitiu dedicar atenção a criação do no novo cluste na gcp.

AWS

Uma vpc duas subnet públicas, uma para o ec2 que hospeda container do sonarqube (sonar, elastic, kinana etc) e uma segunda ec2 que hospeda um servidor mysql. Por que nao rds? Custo. Por que sub net publica? para nao complicar.

GCP

Custer com 4 nodes



To run docker uma locally must set db env
docker run -p5000:5000 --env SQLALCHEMY_DATABASE_URI="mysql+pymysql://revolut:revolut@34.254.242.117/revolut?charset=utf8mb4" scconsulting/hello-python:latest


