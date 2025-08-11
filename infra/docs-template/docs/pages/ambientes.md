# Ambientes

| Ambiente        | _Url_                        | Servidor da Aplicação                   | Servidor do _db_                          |
| --------------- | ---------------------------- | --------------------------------------- | ----------------------------------------- |
| Desenvolvimento | https://tilenedev.mpsp.mp.br | mptilene01d-v.mp.gov.br<br>172.22.0.110 | mpdbtilene01d-v.mp.gov.br<br>192.168.1.81 |
| Homologação     | https://tileneuat.mpsp.mp.br | mptilene01h-v.mp.gov.br<br>172.22.0.108 | mpdbtilene01h-v.mp.sp.gov<br>192.168.1.97 |
| Produção        | https://tilene.mpsp.mp.br    | mptilene01p-v.mp.gov.br                 | mpdbtilene01p-v.mp.sp.gov                 |

<br>

---

## _Hardware_

### Homologação

- 40GB de HD

<br>

---

## Permissionamento

Em conversa com Selma, foi informado que o grupo do _Microsoft Entra ID_, que autoriza o acesso à aplicação, em ambiente de desenvolvimetno e ambiente de homologação é o [Grp_TileneUAT](https://portal.azure.com/#view/Microsoft_AAD_IAM/GroupDetailsMenuBlade/~/Overview/groupId/69135ecb-15ba-4fc7-ae68-bb8b562aac93/menuId/).

???+ question "Dúvida"

    O grupo que acessa o ["ANIA" antigo](https://aniauat.mpsp.mp.br/), instanciado pela *Equipe de Infra*, é o [Grp_AcessaAnia](https://portal.azure.com/#view/Microsoft_AAD_IAM/GroupDetailsMenuBlade/~/Overview/groupId/ff68c26a-e2a9-41f8-ab8d-28efe8d451c1/menuId/) ou é o [Grp_AniaUAT](https://portal.azure.com/#view/Microsoft_AAD_IAM/GroupDetailsMenuBlade/~/Overview/groupId/1d9e132b-d88c-4f02-b058-7130fa26fe9b/menuId/), que tem a descrição _"Grupo para homologar o sistema ANIA"_?
